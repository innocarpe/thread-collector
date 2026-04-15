#!/usr/bin/env python3
"""
ThreadCollector — keyword-based auto-labeler
No AI calls, no external dependencies. Pure Python keyword scoring.

Usage:
  python3 scripts/label.py                        # label all unlabeled posts
  python3 scripts/label.py --all                  # re-label everything
  python3 scripts/label.py --user dalgom.bami     # specific user only
  python3 scripts/label.py --file path/to/post.md # single file
"""

import argparse
import re
import sys
from pathlib import Path

# ── Label taxonomy with keywords ──────────────────────────────────────────────
#
# Each label has a keyword list. keyword_score() counts hits in the post text.
# A label is assigned if its score is above the threshold AND it's among the
# top-scoring labels (up to MAX_LABELS_PER_POST).

MAX_LABELS_PER_POST = 3
MIN_SCORE = 1

LABEL_KEYWORDS: dict[str, list[str]] = {
    "앱개발": [
        "ios", "android", "앱", "app", "모바일", "swift", "kotlin", "flutter",
        "react native", "testflight", "앱스토어", "앱 스토어", "play store", "플레이스토어",
        "xcode", "스크린샷", "apk", "번들", "인앱", "in-app", "애플리케이션",
    ],
    "웹/SaaS": [
        "saas", "웹서비스", "웹 서비스", "웹앱", "웹 앱", "b2b", "구독",
        "랜딩페이지", "랜딩 페이지", "landing page", "대시보드", "dashboard",
        "백엔드", "프론트엔드", "next.js", "nextjs", "react", "vue", "django",
        "supabase", "firebase", "vercel", "aws", "클라우드", "서버리스",
        "api", "saas", "웹훅", "webhook",
    ],
    "AI/LLM": [
        "ai", "인공지능", "llm", "gpt", "chatgpt", "claude", "gemini", "llama",
        "프롬프트", "prompt", "머신러닝", "딥러닝", "embedding", "rag",
        "openai", "anthropic", "파인튜닝", "fine-tuning", "벡터", "agent",
        "챗봇", "chatbot", "자동화", "automation", "코파일럿", "copilot",
    ],
    "개발도구": [
        "vscode", "cursor", "ide", "터미널", "git", "github", "깃허브", "도커", "docker",
        "쿠버네티스", "kubernetes", "ci/cd", "테스트", "lint", "eslint",
        "라이브러리", "프레임워크", "패키지", "npm", "pip", "homebrew",
        "typescript", "javascript", "python", "rust", "go", "java", "개발환경",
        "디버깅", "리팩토링", "코드 리뷰", "pr", "pull request",
    ],
    "마케팅": [
        "마케팅", "광고", "유료", "cpc", "cpm", "roas", "roi", "meta ads",
        "구글 광고", "퍼포먼스", "인플루언서", "콘텐츠 마케팅", "이메일 마케팅",
        "뉴스레터", "newsletter", "캠페인", "홍보", "pr ", "브랜딩", "brand",
        "포지셔닝", "타겟", "세그먼트",
    ],
    "바이럴/SNS": [
        "바이럴", "viral", "sns", "트위터", "twitter", "인스타그램", "instagram",
        "유튜브", "youtube", "틱톡", "tiktok", "릴스", "reels", "쇼츠",
        "팔로워", "follower", "조회수", "좋아요", "공유", "바이럴 마케팅",
        "커뮤니티", "community", "스레드", "threads", "소셜",
    ],
    "ASO/검색": [
        "aso", "키워드", "keyword", "검색어", "검색량", "검색 최적화", "seo",
        "앱스토어 최적화", "구글 플레이", "순위", "랭킹", "노출", "impression",
        "검색 결과", "메타데이터", "설명문", "스크린샷 최적화",
    ],
    "수익화": [
        "수익", "매출", "revenue", "결제", "구독", "subscription", "인앱 결제",
        "price", "가격", "pricing", "무료", "freemium", "프리미엄", "premium",
        "arpu", "ltv", "수익 모델", "monetization", "광고 수익", "커머스",
        "mrr", "arr", "월 매출",
    ],
    "성장전략": [
        "growth", "그로스", "획득", "retention", "리텐션", "churn", "dau", "mau",
        "activation", "kpi", "okr", "지표", "metric", "전환율", "conversion",
        "ab test", "a/b", "실험", "퍼널", "funnel", "onboarding", "온보딩",
        "사용자 수", "성장 전략", "스케일", "scale",
    ],
    "인디해킹": [
        "인디해커", "indie", "1인", "솔로", "solo", "사이드프로젝트", "사이드 프로젝트",
        "side project", "부업", "개인 프로젝트", "인디", "독립", "혼자",
        "indie hacker", "solopreneur", "마이크로 saas", "micro saas",
    ],
    "PMF": [
        "pmf", "product market fit", "제품 시장 적합성", "고객 검증", "검증",
        "인터뷰", "페인포인트", "pain point", "고객 문제", "니즈", "need",
        "피드백", "feedback", "초기 고객", "얼리어답터", "early adopter",
        "피벗", "pivot", "가설", "hypothesis",
    ],
    "제품전략": [
        "로드맵", "roadmap", "기능", "feature", "우선순위", "prioritization",
        "ux", "ui", "사용자 경험", "사용성", "유저 플로우", "와이어프레임",
        "프로토타입", "mvp 이후", "v2", "버전", "제품 결정", "product",
        "프로덕트 매니저", "pm ", "기획", "스펙", "spec",
    ],
    "MVP/런칭": [
        "mvp", "출시", "런칭", "launch", "첫 번째", "첫 버전", "베타", "beta",
        "프로덕트헌트", "product hunt", "론칭", "첫 출시", "v1", "공개",
        "오픈", "런치", "soft launch", "alpha",
    ],
    "스타트업": [
        "스타트업", "startup", "투자", "투자자", "벤처", "vc", "펀딩", "funding",
        "시드", "seed", "시리즈", "series a", "엔젤", "angel", "액셀러레이터",
        "팀", "team", "채용", "hiring", "공동창업자", "co-founder", "cto", "ceo",
        "조직", "문화", "스케일업",
    ],
    "창업철학": [
        "철학", "마인드", "마인드셋", "mindset", "가치관", "원칙", "신념",
        "동기", "why", "이유", "목표", "비전", "mission", "인생", "삶",
        "후회", "결정", "선택", "용기", "실행력", "행동",
    ],
    "개발자커리어": [
        "커리어", "이직", "취업", "면접", "연봉", "salary", "개발자", "engineer",
        "주니어", "시니어", "팀장", "리드", "테크 리드", "매니저", "승진",
        "포트폴리오", "이력서", "resume", "직장", "회사", "스킬",
    ],
    "생산성": [
        "생산성", "productivity", "집중", "포커스", "루틴", "routine", "습관",
        "habit", "시간 관리", "time management", "todo", "플로우", "flow",
        "딥워크", "deep work", "번아웃", "burnout", "에너지", "아침",
    ],
    "학습/스킬": [
        "학습", "공부", "배움", "스터디", "강의", "책", "독서", "튜토리얼",
        "learning", "스킬", "역량", "능력", "성장", "개발자 성장", "실력",
        "코딩 공부", "자격증", "자기계발", "멘토",
    ],
    "회고/인사이트": [
        "회고", "retrospective", "retro", "배운 점", "배운것", "느낀 점",
        "실패", "성공", "경험", "사례", "케이스", "case study", "분석",
        "인사이트", "insight", "정리", "요약", "후기", "review", "결과",
    ],
    # 신규 3개 카테고리 키워드 (2026-04-15)
    "포트폴리오 운영": [
        "다작", "포트폴리오", "대량출시", "자동화", "ci/cd", "350개", "앱 여러개",
        "앱 포트폴리오", "대량 운영", "배치 출시", "자동 배포", "파이프라인",
        "여러 앱", "앱 여러", "mass launch", "앱 운영", "운영 자동화",
    ],
    "ASO/출시전략": [
        "aso", "앱스토어", "키워드 리서치", "플레이스토어 최적화", "설치율",
        "리뷰 대응", "출시 체크리스트", "앱 출시", "검색 순위", "앱스토어 최적화",
        "store listing", "keyword optimization", "앱 노출", "메타데이터",
        "스크린샷 최적화", "앱 설명", "플레이스토어", "app store",
    ],
    "사례연구": [
        "사례", "후기", "리텐션 데이터", "매출 공개", "수익 인증", "앱 실패",
        "postmortem", "case study", "실패 사례", "성공 사례", "수익 데이터",
        "실제 수치", "실제 매출", "dau", "mau", "리텐션", "retention",
        "실패 후기", "앱 분석 사례",
    ],
}

# ── Frontmatter utilities ──────────────────────────────────────────────────────

def read_post_text(path: Path) -> tuple[dict[str, str], str]:
    """Returns (frontmatter_fields, body_text)."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}, raw

    end = raw.find("---", 3)
    if end == -1:
        return {}, raw

    fm_block = raw[3:end]
    body = raw[end + 3:].lstrip("\n")

    fm: dict[str, str] = {}
    for line in fm_block.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")

    return fm, body


def write_labels_to_file(path: Path, labels: list[str]) -> None:
    """Add or replace the `labels` line in a file's YAML frontmatter."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return

    end = raw.find("---", 3)
    if end == -1:
        return

    fm_block = raw[3:end]
    body = raw[end + 3:]

    # Remove existing labels line
    fm_lines = [l for l in fm_block.split("\n") if not l.strip().startswith("labels:")]

    labels_yaml = "labels: [" + ", ".join(f'"{l}"' for l in labels) + "]"
    fm_lines.append(labels_yaml)

    path.write_text("---" + "\n".join(fm_lines) + "\n---" + body, encoding="utf-8")


def already_labeled(path: Path) -> bool:
    fm, _ = read_post_text(path)
    raw = fm.get("labels", "").strip()
    return bool(raw and raw != "[]")


# ── Keyword scoring ────────────────────────────────────────────────────────────

def score_text(text: str) -> dict[str, int]:
    """Return {label: score} for all labels. Score = number of keyword hits."""
    t = text.lower()
    return {
        label: sum(1 for kw in keywords if kw.lower() in t)
        for label, keywords in LABEL_KEYWORDS.items()
    }


def pick_labels(text: str) -> list[str]:
    """Return up to MAX_LABELS_PER_POST labels for the given text."""
    scores = score_text(text)
    qualified = [(label, score) for label, score in scores.items() if score >= MIN_SCORE]
    qualified.sort(key=lambda x: -x[1])
    return [label for label, _ in qualified[:MAX_LABELS_PER_POST]]


# ── Core labeling logic ────────────────────────────────────────────────────────

def label_file(path: Path, force: bool = False) -> list[str]:
    """
    Label a single markdown file. Returns assigned labels.
    Call this from collect.py after saving a post.
    """
    if not force and already_labeled(path):
        fm, _ = read_post_text(path)
        raw = fm.get("labels", "")
        return [l.strip().strip('"') for l in raw.strip("[]").split(",") if l.strip()]

    fm, body = read_post_text(path)
    title = fm.get("title", "")
    full_text = title + "\n" + body

    labels = pick_labels(full_text)
    if labels:
        write_labels_to_file(path, labels)
    return labels


def label_all(threads_root: Path, user: str | None = None, force: bool = False) -> tuple[int, int]:
    """
    Label all posts under threads_root.
    Returns (labeled_count, skipped_count).
    """
    pattern = f"{user}/**/*.md" if user else "**/*.md"
    files = sorted(threads_root.glob(pattern))

    if not files:
        return 0, 0

    labeled = 0
    skipped = 0

    for path in files:
        if not force and already_labeled(path):
            skipped += 1
            continue

        fm, body = read_post_text(path)
        full_text = body
        labels = pick_labels(full_text)

        if labels:
            write_labels_to_file(path, labels)
            labeled += 1
        else:
            skipped += 1

    return labeled, skipped


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Keyword-based auto-labeler for ThreadCollector posts. No AI, no API calls."
    )
    p.add_argument("--all", action="store_true", help="Re-label already-labeled posts.")
    p.add_argument("--user", default=None, help="Only label posts from this user, e.g. dalgom.bami")
    p.add_argument("--file", default=None, help="Label a single markdown file.")
    p.add_argument(
        "--threads-dir",
        dest="threads_dir",
        default=None,
        help="Root dir of collected posts (default: Threads/ in CWD).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    threads_root = Path(args.threads_dir) if args.threads_dir else Path.cwd() / "Threads"

    if args.file:
        path = Path(args.file)
        if not path.exists():
            sys.exit(f"ERROR: 파일 없음: {path}")
        labels = label_file(path, force=args.all)
        print(f"{path.name}: {labels if labels else '(레이블 없음)'}")
        return

    if not threads_root.exists():
        sys.exit(f"ERROR: 디렉토리 없음: {threads_root}")

    scope = f"@{args.user}" if args.user else "전체"
    print(f"ThreadCollector 레이블러 (키워드 기반)")
    print(f"  범위: {scope}")
    print(f"  모드: {'전체 재처리' if args.all else '미처리 파일만'}")
    print()

    labeled, skipped = label_all(threads_root, user=args.user, force=args.all)

    print(f"완료: {labeled}개 파일 레이블링, {skipped}개 스킵")


if __name__ == "__main__":
    # repo 루트를 sys.path에 추가 (직접 실행 시 sources 패키지 import 보장)
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    main()
