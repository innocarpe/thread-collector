#!/usr/bin/env python3
"""
NaverCafe Collector — 네이버 카페 게시글 수집기
Usage:
  python3 scripts/collect_naver.py vibemoney                     # 핵심 게시판 전체
  python3 scripts/collect_naver.py vibemoney --only-menus 22,8   # 특정 게시판만
  python3 scripts/collect_naver.py vibemoney --list-menus        # 게시판 목록 출력

저장 구조:
  NaverCafe/{cafe}/operator/{category}/  — 운영자 글
  NaverCafe/{cafe}/community/{category}/ — 일반 유저 글
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("ERROR: requests 미설치. pip install requests")

try:
    import pycookiecheat
except ImportError:
    sys.exit("ERROR: pycookiecheat 미설치. pip install pycookiecheat")

# ── Constants ─────────────────────────────────────────────────────────────────

BASE_URL = "https://apis.naver.com/cafe-web"

CHROME_PROFILE_PATHS = [
    "~/Library/Application Support/Google/Chrome/Profile 7/Cookies",
    "~/Library/Application Support/Google/Chrome/Profile 2/Cookies",
    "~/Library/Application Support/Google/Chrome/Default/Cookies",
    "~/Library/Application Support/Chromium/Default/Cookies",
    "~/.config/google-chrome/Default/Cookies",
]

CATEGORY_LABELS = {
    "income-methods": "수익화 방법",
    "tools-ai":       "도구/AI/자동화",
    "case-studies":   "성공 사례/후기",
    "marketing":      "마케팅/콘텐츠",
    "uncategorized":  "미분류",
}

# 카페별 운영자 닉네임
CAFE_OPERATORS = {
    "vibemoney": {"만능시바", "만렙시바"},
}

KNOWN_CAFES = {
    "vibemoney": "31623270",
}

# 카페별 게시판 목록 (menuId → 이름)
KNOWN_MENUS = {
    "vibemoney": {
        # ── 핵심 수집 대상 ──────────────────────────────
        7:  "⌨️ AI 바이브 코딩 가이드",
        8:  "💰 수익화 후기",
        9:  "📊 마케팅 가이드",
        22: "💰 수익화 가이드",
        29: "🔨 작업물 공유하기",
        30: "💡 바이브 코딩 꿀팁 공유",
        31: "💰 바이브머니 수강 후기",
        # ── 수집 대상 (커뮤니티 콘텐츠) ─────────────────
        1:  "💬 QnA",
        4:  "🎁 운영중인 서비스 홍보",
        12: "💡 개발 프로젝트 제안",
        32: "📰 최신 바이브 코딩 뉴스",
        # ── 스킵 권장 ───────────────────────────────────
        5:  "📣 본인 SNS 채널 홍보",
        6:  "🚩 베타테스터 모집",
        13: "💼 프리랜서 구직글",
        14: "👋 가입인사",
        23: "공지사항",
        26: "🎁 준비중인 서비스 홍보",
        28: "📚 과제 게시판",
        34: "👨‍👩‍👦 행사 안내",
        36: "👕 기타 상품 홍보",
    }
}

# 기본 수집 게시판 (--only-menus 미지정 시)
DEFAULT_MENUS = {
    "vibemoney": {1, 4, 7, 8, 9, 22, 23, 29, 30, 31},
}

# ── 키워드 분류기 ─────────────────────────────────────────────────────────────

INCOME_KEYWORDS = [
    "수익", "수익화", "돈", "월급", "월수입", "매출", "부수입", "부업",
    "수입", "벌다", "벌었", "번다", "만원", "억", "천만", "수익률",
    "셀링", "판매", "클라이언트", "외주", "프리랜서", "단가", "견적",
    "passive income", "패시브", "자동화 수익",
    "전자책", "ebook", "강의", "코스", "온라인 판매", "디지털 상품",
    "블로그 수익", "유튜브 수익", "sns 수익", "광고 수익",
    "제휴 마케팅", "어필리에이트", "affiliate", "크몽", "토스페이",
]

TOOLS_KEYWORDS = [
    "ai", "인공지능", "llm", "gpt", "claude", "gemini", "cursor", "copilot",
    "자동화", "automation", "n8n", "make.com", "zapier", "워크플로우",
    "vibe coding", "바이브코딩", "vibe", "노코드", "로우코드",
    "오픈클로", "openclaw", "claude code", "안티그래비티", "antigravity",
    "앱", "웹사이트", "랜딩페이지", "saas",
    "파이썬", "python", "javascript", "typescript", "스크립트",
    "api", "webhook", "크롤링", "스크래핑", "봇", "bot",
    "프롬프트", "prompt", "chatgpt", "perplexity", "grok",
    "erp", "대시보드", "자동매매", "알고리즘",
]

CASE_KEYWORDS = [
    "후기", "사례", "성공", "경험", "실제", "해봤", "해봤더니",
    "결과", "달성", "인증", "처음으로", "만에", "수강", "강의 후기",
    "따라서", "따라하면", "실천", "적용",
]

MARKETING_KEYWORDS = [
    "마케팅", "marketing", "콘텐츠", "content", "글쓰기", "카피",
    "sns", "인스타", "instagram", "유튜브", "youtube", "틱톡",
    "트위터", "x.com", "스레드", "threads", "링크드인",
    "팔로워", "구독자", "채널", "브랜딩", "퍼스널 브랜드",
    "바이럴", "알고리즘", "노출", "도달", "광고", "ads",
    "seo", "키워드", "이메일", "뉴스레터", "퍼널", "리드",
    "숏폼", "쇼츠", "릴스",
]


def keyword_score(text: str, keywords: list[str]) -> int:
    t = text.lower()
    return sum(1 for kw in keywords if kw.lower() in t)


def categorize(subject: str, content: str) -> str:
    combined = f"{subject} {content}".lower()
    scores = {
        "income-methods": keyword_score(combined, INCOME_KEYWORDS),
        "tools-ai":       keyword_score(combined, TOOLS_KEYWORDS),
        "case-studies":   keyword_score(combined, CASE_KEYWORDS),
        "marketing":      keyword_score(combined, MARKETING_KEYWORDS),
    }
    mx = max(scores.values())
    if mx == 0:
        return "uncategorized"
    return max(scores, key=lambda k: scores[k])


# ── clubId 자동 탐색 ──────────────────────────────────────────────────────────

def discover_club_id(cafe_name: str) -> str | None:
    """카페 메인 페이지 HTML에서 clubId 자동 추출."""
    import re as _re
    url = f"https://cafe.naver.com/{cafe_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9",
    }
    try:
        r = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        html = r.text
    except Exception:
        return None

    # 패턴 1: iframe src에 clubid=XXXXXXXX
    m = _re.search(r"clubid=(\d+)", html, _re.IGNORECASE)
    if m:
        return m.group(1)

    # 패턴 2: JS 변수 cafeId / clubId / cafe_club_id
    m = _re.search(r"""(?:cafeId|clubId|cafe_club_id)['":\s=]+(\d{6,12})""", html, _re.IGNORECASE)
    if m:
        return m.group(1)

    # 패턴 3: JSON 형태 "clubId":"XXXXXXXX"
    m = _re.search(r'"clubId"\s*:\s*"?(\d{6,12})"?', html)
    if m:
        return m.group(1)

    return None


# ── 쿠키 / 헤더 ───────────────────────────────────────────────────────────────

def load_cookies(cafe_url: str) -> dict:
    for raw_path in CHROME_PROFILE_PATHS:
        p = os.path.expanduser(raw_path)
        if not os.path.isfile(p):
            continue
        try:
            cookies = pycookiecheat.chrome_cookies(cafe_url, cookie_file=p)
            if cookies:
                print(f"  [쿠키] {p} → {len(cookies)}개 로드")
                return cookies
        except Exception:
            continue
    print("  [경고] 쿠키 없음. 비로그인 상태로 시도합니다.")
    return {}


def make_headers(cafe_name: str) -> dict:
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://cafe.naver.com/{cafe_name}",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://cafe.naver.com",
        "Accept-Language": "ko-KR,ko;q=0.9",
    }


# ── API ───────────────────────────────────────────────────────────────────────

def get_article_list(club_id: str, menu_id: int, page: int, page_size: int,
                     cookies: dict, headers: dict) -> dict | None:
    url = f"{BASE_URL}/cafe-boardlist-api/v1/cafes/{club_id}/menus/{menu_id}/articles"
    params = {"page": page, "pageSize": page_size, "sortBy": "TIME", "viewType": "L"}
    try:
        r = requests.get(url, params=params, cookies=cookies, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json().get("result")
        return None
    except Exception:
        return None


def get_article_detail(club_id: str, article_id: int,
                       cookies: dict, headers: dict) -> dict | None:
    url = f"{BASE_URL}/cafe-articleapi/v2.1/cafes/{club_id}/articles/{article_id}"
    try:
        r = requests.get(url, cookies=cookies, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json().get("result", {}).get("article")
        return None
    except Exception:
        return None


# ── HTML → text ───────────────────────────────────────────────────────────────

def html_to_text(html: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<p[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = (text
            .replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">")
            .replace("&amp;", "&").replace("&quot;", '"')
            .replace("&#x27;", "'").replace("&#39;", "'"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ── 저장 ──────────────────────────────────────────────────────────────────────

def make_slug(text: str, max_len: int = 40) -> str:
    first = re.split(r"[.!?\n\[\]]", text.strip())[0].strip()[:max_len]
    slug = re.sub(r"[^\w가-힣]+", "-", first, flags=re.UNICODE)
    return slug.strip("-").lower() or "post"


def save_article(article_id: int, subject: str, content: str,
                 writer: str, write_date_ms: int, menu_name: str,
                 cafe_name: str, category: str, segment: str,
                 output_root: Path) -> Path:
    """
    segment: 'operator' | 'community'
    저장 경로: {output_root}/{cafe_name}/{segment}/{category}/{date}-{slug}.md
    """
    dt = datetime.fromtimestamp(write_date_ms / 1000, tz=timezone.utc)
    date_str = dt.strftime("%Y-%m-%d")
    slug = make_slug(subject)

    cat_dir = output_root / cafe_name / segment / category
    cat_dir.mkdir(parents=True, exist_ok=True)

    filepath = cat_dir / f"{date_str}-{slug}.md"
    counter = 1
    while filepath.exists():
        # 같은 날짜+슬러그지만 다른 article_id면 suffix
        existing = filepath.read_text(encoding="utf-8")
        if f"article_id: {article_id}" in existing:
            return filepath  # 이미 같은 글, 덮어쓰기 방지
        filepath = cat_dir / f"{date_str}-{slug}-{counter}.md"
        counter += 1

    lines = [
        "---",
        f"article_id: {article_id}",
        f'cafe: "{cafe_name}"',
        f'segment: "{segment}"',
        f'category: "{CATEGORY_LABELS[category]}"',
        f'menu: "{menu_name}"',
        f'writer: "{writer}"',
        f"write_date_ms: {write_date_ms}",
        f'date: "{date_str}"',
        f'source: "https://cafe.naver.com/{cafe_name}/{article_id}"',
        "---",
        "",
        f"# {subject}",
        "",
        content,
        "",
    ]
    filepath.write_text("\n".join(lines), encoding="utf-8")
    return filepath


# ── 수집 코어 ─────────────────────────────────────────────────────────────────

def collect_menu(club_id: str, menu_id: int, menu_name: str,
                 max_pages: int, page_size: int,
                 cafe_name: str, operators: set[str],
                 output_root: Path,
                 cookies: dict, headers: dict,
                 article_ids_seen: set[int],
                 stats: dict) -> None:

    for page in range(1, max_pages + 1):
        result = get_article_list(club_id, menu_id, page, page_size, cookies, headers)
        if result is None:
            print(f"    Page {page}: API 실패")
            break

        articles = result.get("articleList", [])
        page_info = result.get("pageInfo", {})

        if page == 1:
            total = page_info.get("totalArticleCount", "?")
            last = page_info.get("lastNavigationPageNumber", "?")
            print(f"    게시글 수: {total}  (마지막 페이지: {last})")

        if not articles:
            break

        for item_wrap in articles:
            item = item_wrap.get("item", {})
            article_id = item.get("articleId")
            if not article_id or article_id in article_ids_seen:
                continue
            article_ids_seen.add(article_id)

            subject = item.get("subject", "")
            writer_nick = item.get("writerInfo", {}).get("nickName", "")
            write_ts = item.get("writeDateTimestamp", 0)

            detail = get_article_detail(club_id, article_id, cookies, headers)
            if detail is None:
                stats["_skipped"] = stats.get("_skipped", 0) + 1
                continue

            content = html_to_text(detail.get("contentHtml", ""))
            actual_writer = detail.get("writer", {}).get("nick", writer_nick)
            actual_menu = detail.get("menu", {}).get("name", menu_name)

            segment = "operator" if actual_writer in operators else "community"
            category = categorize(subject, content)

            save_article(
                article_id=article_id,
                subject=subject,
                content=content,
                writer=actual_writer,
                write_date_ms=write_ts,
                menu_name=actual_menu,
                cafe_name=cafe_name,
                category=category,
                segment=segment,
                output_root=output_root,
            )

            key = f"{segment}/{category}"
            stats[key] = stats.get(key, 0) + 1

            seg_tag = "★운영자" if segment == "operator" else "  일반"
            print(f"      {seg_tag} [{article_id}] [{category}] {subject[:45]}")

            time.sleep(0.2)

        last_nav = page_info.get("lastNavigationPageNumber", page)
        has_more = page_info.get("visibleNextButton", False)
        if page >= last_nav and not has_more:
            break

        time.sleep(0.5)


def collect(cafe_name: str, club_id: str,
            target_menus: dict[int, str],
            max_pages: int, page_size: int,
            output_root: Path) -> None:

    cafe_url = f"https://cafe.naver.com/{cafe_name}"
    cookies = load_cookies(cafe_url)
    headers = make_headers(cafe_name)
    operators = CAFE_OPERATORS.get(cafe_name, set())

    stats: dict[str, int] = {}
    article_ids_seen: set[int] = set()

    print(f"\n[수집 시작]")
    print(f"  카페     : {cafe_name} (clubId={club_id})")
    print(f"  운영자   : {operators}")
    print(f"  게시판   : {len(target_menus)}개")
    print(f"  최대 페이지/게시판: {max_pages}")

    for mid, mname in sorted(target_menus.items()):
        print(f"\n  [{mid}] {mname}")
        collect_menu(
            club_id=club_id, menu_id=mid, menu_name=mname,
            max_pages=max_pages, page_size=page_size,
            cafe_name=cafe_name, operators=operators,
            output_root=output_root,
            cookies=cookies, headers=headers,
            article_ids_seen=article_ids_seen,
            stats=stats,
        )

    # 결과 리포트
    skipped = stats.pop("_skipped", 0)
    total = sum(stats.values())

    print(f"\n{'='*55}")
    print(f"NaverCafe Collector 완료 — {cafe_name}")
    print(f"  수집: {total}개  건너뜀(401 등): {skipped}개")
    print()

    op_total = sum(v for k, v in stats.items() if k.startswith("operator/"))
    cm_total = sum(v for k, v in stats.items() if k.startswith("community/"))
    print(f"  ★ 운영자  : {op_total}개")
    for cat, label in CATEGORY_LABELS.items():
        k = f"operator/{cat}"
        if stats.get(k, 0):
            print(f"      {output_root/cafe_name/'operator'/cat}/  ({stats[k]}개)")
    print(f"     일반   : {cm_total}개")
    for cat, label in CATEGORY_LABELS.items():
        k = f"community/{cat}"
        if stats.get(k, 0):
            print(f"      {output_root/cafe_name/'community'/cat}/  ({stats[k]}개)")


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="NaverCafe Collector — 운영자/커뮤니티 분리 수집"
    )
    parser.add_argument("cafe_name", help="카페 슬러그 (예: vibemoney)")
    parser.add_argument("--club-id", dest="club_id", default=None)
    parser.add_argument("--limit", type=int, default=200,
                        help="게시판당 최대 페이지. 기본값: 200")
    parser.add_argument("--page-size", dest="page_size", type=int, default=20)
    parser.add_argument("--only-menus", dest="only_menus", default="",
                        help="특정 게시판만 (쉼표 구분). 예: --only-menus 22,8")
    parser.add_argument("--list-menus", dest="list_menus", action="store_true")
    parser.add_argument("--output-dir", dest="output_dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cafe_name = args.cafe_name.strip().lower()

    club_id = args.club_id or KNOWN_CAFES.get(cafe_name)
    if not club_id:
        print(f"  [clubId] '{cafe_name}' 자동 탐색 중 ...")
        club_id = discover_club_id(cafe_name)
        if club_id:
            print(f"  [clubId] 발견: {club_id}")
        else:
            sys.exit(
                f"ERROR: '{cafe_name}' clubId 자동 탐색 실패.\n"
                f"  직접 지정: python3 scripts/collect_naver.py {cafe_name} --club-id XXXXXXXX\n"
                f"  카페 URL: https://cafe.naver.com/{cafe_name}"
            )

    output_root = Path(args.output_dir) if args.output_dir else Path.cwd() / "NaverCafe"

    if args.list_menus:
        known = KNOWN_MENUS.get(cafe_name, {})
        print(f"\n{cafe_name} 게시판 목록:")
        for mid, name in sorted(known.items()):
            print(f"  [{mid:2d}] {name}")
        return

    # 수집 게시판 결정
    if args.only_menus:
        ids = {int(s.strip()) for s in args.only_menus.split(",") if s.strip().isdigit()}
        menus_map = KNOWN_MENUS.get(cafe_name, {})
        target_menus = {mid: menus_map.get(mid, f"board-{mid}") for mid in ids}
    else:
        defaults = DEFAULT_MENUS.get(cafe_name, set())
        menus_map = KNOWN_MENUS.get(cafe_name, {})
        target_menus = {mid: menus_map[mid] for mid in defaults if mid in menus_map}

    collect(
        cafe_name=cafe_name,
        club_id=club_id,
        target_menus=target_menus,
        max_pages=args.limit,
        page_size=min(args.page_size, 50),
        output_root=output_root,
    )


if __name__ == "__main__":
    main()
