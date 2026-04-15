#!/usr/bin/env python3
"""
ThreadCollector — 블로그 글 AI 분류
Usage: python3 -m sources.blog.classify --creator programmingzombie
       python3 -m sources.blog.classify --creator programmingzombie --only-uncategorized
       python3 -m sources.blog.classify --all

Blog/{creator}/**/uncategorized/*.md 글을 codex exec으로 분류해
primary 카테고리 폴더로 이동. frontmatter에 categories: [primary, ...] 갱신.

Notes:
- codex None 응답 시 파일 삭제/수정 금지 — uncategorized/ 에 그대로 남겨 재시도
- 블로그는 여러 카테고리 허용: primary 1개 + secondary ≤2개
- frontmatter 필드: categories: [primary, sub1, sub2]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# repo 루트를 sys.path에 추가 (직접 실행 및 -m 호출 모두 지원)
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sources._common.codex import find_codex

# 13-category (types/post.ts와 일치)
CATEGORY_LABELS = {
    "ai-llm": "AI/LLM",
    "viral-sns": "바이럴/SNS/마케팅",
    "monetization": "수익화/부수입",
    "dev-tools": "개발도구/스택",
    "product-strategy": "제품전략/PMF",
    "startup-philosophy": "창업철학/인디해킹",
    "career-growth": "커리어/성장",
    "learning-retro": "학습/회고",
    "productivity": "생산성/워크플로우",
    "web-app": "웹/앱 개발",
    # 신규 3개 (2026-04-15)
    "portfolio-ops": "포트폴리오 운영",
    "aso": "ASO/출시전략",
    "case-study": "사례연구",
}

CATEGORY_DESCRIPTIONS = {
    "ai-llm": "LLM/생성형 AI 활용, 프롬프트 엔지니어링, AI 제품/도구 리뷰, 바이브코딩",
    "viral-sns": "SNS 콘텐츠 전략, 바이럴 기법, 쇼츠·릴스·스레드 운영, 알고리즘, ASO/검색, 퍼널 마케팅",
    "monetization": "수익화 실험, 부수입, 광고수익, 가격 실험, 캐시플로우·매출 인증",
    "dev-tools": "개발 도구·에디터·CLI·스택 선택·빌드 파이프라인·워크플로우 최적화",
    "product-strategy": "제품 전략, PMF 탐색, MVP 기획, 피봇, 유저 리서치, 기능 우선순위",
    "startup-philosophy": "창업 마인드셋, 인디해킹 철학, 실패·번아웃 후기, 스타트업 인사이트",
    "career-growth": "커리어 전환, 이직·취업, 개발자·창업자 성장, 연봉·포트폴리오",
    "learning-retro": "학습법, 스킬 향상, 공부 후기, 회고, 일·프로젝트 인사이트 요약",
    "productivity": "생산성, 루틴, 타임박싱, 셀프 매니지먼트, 집중력, 업무 효율",
    "web-app": "웹/SaaS 개발, 앱 개발, 프론트/백엔드 구체 기술, 배포·인프라",
    "portfolio-ops": "다작·자동화·CI/CD·앱 포트폴리오 대량 운영 체계, 350앱 운영 철학, 대량출시 전략",
    "aso": "앱스토어 최적화, 키워드 리서치, 출시 체크리스트, 리뷰 대응, 플레이스토어 순위 전략",
    "case-study": "특정 앱 성공/실패 사례, 수익 인증, 리텐션 실데이터, postmortem, 실패 후기",
}

# 한 배치에 처리할 최대 글 수
CLASSIFY_BATCH_SIZE = 20  # 블로그 글은 Threads보다 길어 배치 크기를 작게


def parse_blog_post(filepath: Path) -> dict | None:
    """블로그 markdown 파일에서 slug, title, 본문 첫 500자 추출."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    # frontmatter 파싱
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    fm_text = parts[1]
    body = parts[2].strip()

    # source: blog 또는 sourceType: blog 필드 확인 (블로그 글만 처리)
    is_blog = re.search(r'^source(?:Type)?:\s*["\']?blog["\']?', fm_text, re.MULTILINE | re.IGNORECASE)
    if not is_blog:
        # sourceType이 없어도 creator 필드가 있으면 블로그 글로 간주
        has_creator = re.search(r'^creator:', fm_text, re.MULTILINE)
        if not has_creator:
            return None

    # 기존에 categories가 이미 분류된 경우 uncategorized 확인
    cat_match = re.search(r'^categories:\s*\[([^\]]*)\]', fm_text, re.MULTILINE)
    if cat_match:
        cats_str = cat_match.group(1).strip()
        if cats_str and cats_str not in ('', '"uncategorized"', 'uncategorized'):
            # uncategorized가 아닌 실제 카테고리가 있으면 skip
            cats = [c.strip().strip('"\'') for c in cats_str.split(',') if c.strip()]
            real_cats = [c for c in cats if c and c != 'uncategorized']
            if real_cats:
                return None  # 이미 분류됨

    # 제목 추출
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm_text, re.MULTILINE)
    title = title_match.group(1) if title_match else ""

    # 본문 첫 500자 (분류 프롬프트용)
    text_preview = body[:500] if body else title

    return {
        "slug": filepath.stem,
        "title": title,
        "text": text_preview,
        "filepath": filepath,
        "content": content,
        "frontmatter": fm_text,
    }


def codex_classify_blog(posts: list[dict]) -> dict[str, dict]:
    """
    codex exec으로 블로그 글 분류.
    반환: {slug: {"primary": str, "secondary": list[str]}}
    codex 실패 시 빈 dict 반환 — 호출 측에서 None으로 처리해 파일을 건드리지 않음.
    """
    if not posts:
        return {}

    codex = find_codex()
    if not codex:
        print("[warn] codex not found — AI 분류를 건너뜁니다")
        return {}

    result: dict[str, dict] = {}
    total_batches = (len(posts) + CLASSIFY_BATCH_SIZE - 1) // CLASSIFY_BATCH_SIZE

    for batch_idx in range(total_batches):
        batch = posts[batch_idx * CLASSIFY_BATCH_SIZE : (batch_idx + 1) * CLASSIFY_BATCH_SIZE]
        batch_num = batch_idx + 1
        print(f"  Batch {batch_num}/{total_batches}: {len(batch)} posts ...", end="", flush=True)

        tmp_input = f"/tmp/tc_blog_classify_in_{batch_idx}.json"
        tmp_output = f"/tmp/tc_blog_classify_out_{batch_idx}.json"

        with open(tmp_input, "w", encoding="utf-8") as f:
            json.dump(
                [{"slug": p["slug"], "title": p["title"], "text": p["text"]} for p in batch],
                f, ensure_ascii=False, indent=2,
            )

        cat_lines = "\n".join(
            f'- "{slug}": {CATEGORY_DESCRIPTIONS[slug]}'
            for slug in CATEGORY_LABELS
        )
        prompt = (
            f"Read {tmp_input} — JSON array of blog posts (slug + title + text, Korean/English).\n\n"
            "Classify each post. Blog posts may span multiple topics.\n\n"
            "For each post assign:\n"
            "  - primary: ONE best-fit category slug\n"
            "  - secondary: UP TO 2 additional category slugs (can be empty list)\n\n"
            "Available categories:\n"
            f"{cat_lines}\n"
            '- "skip": junk — no technical/business insight, purely personal diary with no actionable content\n\n'
            "Rules:\n"
            "- primary is the single BEST fit (what the post is MAINLY about).\n"
            "- secondary captures meaningful secondary themes only — if a post is clearly one topic, secondary=[]\n"
            "- AI 도구·LLM 제품에 관한 리뷰·사용기는 primary='ai-llm' 우선.\n"
            "- 수익 인증·실데이터가 포함된 사례는 'case-study' 또는 'monetization' 우선.\n"
            "- 앱스토어 최적화·키워드 리서치는 'aso'.\n"
            "- 포트폴리오 대량 운영·CI/CD 파이프라인은 'portfolio-ops'.\n\n"
            f"Write ONLY a JSON file to {tmp_output}:\n"
            '[{"slug": "...", "primary": "...", "secondary": ["...", "..."]}]\n'
            "No explanation. Only write the JSON file."
        )

        proc = None
        try:
            # 이전 배치의 stale 출력 제거
            if os.path.isfile(tmp_output):
                os.unlink(tmp_output)
            proc = subprocess.run(
                [codex, "exec", "--full-auto", "--ephemeral",
                 "--model", "gpt-5.4-mini",
                 "--add-dir", "/tmp",
                 prompt],
                capture_output=True, text=True, timeout=180,
            )
        except subprocess.TimeoutExpired:
            print(" timeout")
            continue

        classified_count = 0
        if os.path.isfile(tmp_output):
            try:
                raw = open(tmp_output, encoding="utf-8").read().strip()
                m = re.search(r"\[.*\]", raw, re.DOTALL)
                if m:
                    items = json.loads(m.group())
                    for item in items:
                        slug = item.get("slug", "")
                        primary = item.get("primary", "")
                        secondary = item.get("secondary", [])
                        if slug and primary:
                            result[slug] = {
                                "primary": primary,
                                "secondary": [s for s in secondary if s in CATEGORY_LABELS],
                            }
                    classified_count = sum(1 for p in batch if p["slug"] in result)
            except Exception:
                pass

        if classified_count:
            print(f" {classified_count} classified")
        else:
            print(" parse failed")
            if proc and proc.stderr:
                tail = "\n".join(proc.stderr.strip().splitlines()[-5:])
                if tail:
                    print(f"    codex stderr (tail):\n    {tail}")
            if proc and proc.stdout:
                tail = "\n".join(proc.stdout.strip().splitlines()[-5:])
                if tail and "ERROR" in tail.upper():
                    print(f"    codex stdout (tail):\n    {tail}")

    return result


def update_frontmatter_categories(content: str, fm_text: str, categories: list[str]) -> str:
    """frontmatter의 categories 필드를 갱신한 전체 파일 내용 반환."""
    cats_yaml = "[" + ", ".join(f'"{c}"' for c in categories) + "]"

    # 기존 categories 필드 교체 또는 추가
    if re.search(r'^categories:', fm_text, re.MULTILINE):
        new_fm = re.sub(
            r'^categories:.*$',
            f'categories: {cats_yaml}',
            fm_text,
            flags=re.MULTILINE,
        )
    else:
        # categories 필드가 없으면 frontmatter 끝에 추가
        new_fm = fm_text.rstrip() + f'\ncategories: {cats_yaml}\n'

    return content.replace(fm_text, new_fm, 1)


def move_to_primary(post_data: dict, primary: str, secondary: list[str], blog_root: Path, creator: str) -> None:
    """
    uncategorized/ 의 파일을 primary 카테고리 폴더로 이동.
    frontmatter의 categories 필드를 [primary, ...secondary] 로 갱신.
    """
    categories = [primary] + secondary
    new_content = update_frontmatter_categories(
        post_data["content"], post_data["frontmatter"], categories
    )

    target_dir = blog_root / creator / primary
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / post_data["filepath"].name
    target_path.write_text(new_content, encoding="utf-8")
    post_data["filepath"].unlink()


def classify_creator(creator: str, blog_root: Path, only_uncategorized: bool = True) -> None:
    """단일 creator의 블로그 글을 분류."""
    creator_dir = blog_root / creator

    if not creator_dir.exists():
        print(f"[skip] Blog/{creator}/ 없음 — 수집 먼저 실행")
        return

    # 대상 파일 수집
    if only_uncategorized:
        # uncategorized/ 폴더만
        uncat_dir = creator_dir / "uncategorized"
        if not uncat_dir.exists():
            print(f"[{creator}] uncategorized/ 없음 — 이미 분류 완료")
            return
        md_files = sorted(uncat_dir.glob("*.md"))
    else:
        # 모든 카테고리 폴더 포함 (재분류)
        md_files = sorted(creator_dir.rglob("*.md"))
        # insights/ 폴더 제외
        md_files = [f for f in md_files if "insights" not in f.parts]

    if not md_files:
        print(f"[{creator}] 분류할 파일 없음")
        return

    print(f"\nBlogClassify — {creator}")
    print(f"  대상: {len(md_files)} 파일")

    posts = [d for f in md_files if (d := parse_blog_post(f)) is not None]
    if not posts:
        print(f"  분류 가능한 포스트 없음 (already classified or invalid format)")
        return

    print(f"  파싱: {len(posts)} posts → codex 분류 중...")
    slug_map = codex_classify_blog(posts)

    print(f"\n  분류 적용 중...")
    stats = {cat: 0 for cat in CATEGORY_LABELS}
    skipped = 0
    unresolved = 0
    failed = 0

    for post in posts:
        classification = slug_map.get(post["slug"])

        if classification is None:
            # codex가 이 글에 대한 결과를 반환하지 않음
            # 치명 버그 패턴 방지: 파일을 절대 건드리지 않음
            unresolved += 1
        elif classification.get("primary") == "skip":
            # 명시적 junk → 삭제
            post["filepath"].unlink()
            skipped += 1
        elif classification.get("primary") in CATEGORY_LABELS:
            primary = classification["primary"]
            secondary = classification.get("secondary", [])
            move_to_primary(post, primary, secondary, blog_root, creator)
            stats[primary] += 1
        else:
            # 알 수 없는 카테고리 → 파일 그대로 유지
            failed += 1

    if unresolved:
        print(
            f"  [warn] {unresolved} posts left in uncategorized/ — codex 결과 없음 "
            f"(rate limit? timeout?). /classify 재실행으로 retry 가능."
        )

    # uncategorized/ 가 비었으면 디렉토리 정리
    uncat_dir = creator_dir / "uncategorized"
    if uncat_dir.exists():
        try:
            uncat_dir.rmdir()
        except OSError:
            remaining = len(list(uncat_dir.glob("*.md")))
            if remaining:
                print(f"  {remaining} posts left unclassified in uncategorized/")

    print(f"\nBlogClassify 완료 — {creator}")
    for cat in CATEGORY_LABELS:
        if stats[cat]:
            print(f"  → {cat}/  +{stats[cat]}")
    print(f"  Skipped (junk): {skipped}")
    if failed:
        print(f"  Failed (unknown category): {failed}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="블로그 글을 13-category로 AI 분류 (codex exec)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--creator", help="Creator slug, 예: programmingzombie")
    group.add_argument("--all", action="store_true", help="Blog/ 하위 전체 creator 처리")
    parser.add_argument(
        "--only-uncategorized",
        dest="only_uncategorized",
        action="store_true",
        default=True,
        help="uncategorized/ 폴더만 처리 (기본값). --no-only-uncategorized로 전체 재분류.",
    )
    parser.add_argument(
        "--no-only-uncategorized",
        dest="only_uncategorized",
        action="store_false",
    )
    parser.add_argument("--blog-dir", dest="blog_dir", default=None,
                        help="Blog/ 루트 경로 (기본: repo 루트의 Blog/)")
    args = parser.parse_args()

    blog_root = Path(args.blog_dir) if args.blog_dir else Path.cwd() / "Blog"

    if args.all:
        if not blog_root.exists():
            sys.exit(f"Blog/ 디렉토리 없음: {blog_root}")
        creators = [d.name for d in sorted(blog_root.iterdir()) if d.is_dir()]
        if not creators:
            sys.exit("Blog/ 에 creator 디렉토리 없음")
        print(f"전체 creator 처리: {creators}")
        for creator in creators:
            classify_creator(creator, blog_root, args.only_uncategorized)
    else:
        classify_creator(args.creator, blog_root, args.only_uncategorized)


if __name__ == "__main__":
    main()
