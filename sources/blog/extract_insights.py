#!/usr/bin/env python3
"""
ThreadCollector — 블로그 글 1개당 구조화 인사이트 추출
Usage: python3 -m sources.blog.extract_insights --creator programmingzombie
       python3 -m sources.blog.extract_insights --creator programmingzombie --slug 2024-12-01-foo
       python3 -m sources.blog.extract_insights --creator programmingzombie --skip-existing

입력:  Blog/{creator}/{category}/{slug}.md (frontmatter + 본문)
출력:  Blog/{creator}/insights/{slug}-insight.md

Notes:
- codex None 응답 시 파일 삭제/수정 금지 — skip 후 재시도 가능
- --skip-existing: 이미 insight 파일이 존재하면 건너뜀
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

# repo 루트를 sys.path에 추가
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sources._common.codex import find_codex

# codex 추출 요청 프롬프트 (한국어)
EXTRACT_PROMPT_TEMPLATE = """당신은 인디 개발자 블로그 글을 분석하는 리서처입니다.
아래 글을 읽고 정해진 YAML 프론트매터 + 섹션 구조로 구조화 인사이트를 추출하세요.
반드시 한국어로 작성합니다.
핵심 주장은 원문에 근거해야 하고, 공개된 숫자·지표는 원문에 명시된 것만 추출합니다(추측 금지).
복제 가능한 전술은 실행 가능한 수준으로 구체화하되 원문에 없는 수치는 만들지 마세요.

입력 파일: {input_path}
출력 파일: {output_path}

출력 파일 형식은 다음 템플릿을 정확히 따르세요:

---
source: blog
creator: {creator}
url: {url}
title: {title}
published_at: {published_at}
collected_at: {collected_at}
categories: {categories}
insight_extracted_at: {today}
---

## 핵심 주장 (≤5)
1. {{주장 - 원문 인용 가능}}
(원문에 주장이 부족하면 더 적게)

## 공개된 숫자·지표
- {{지표}}: {{값}} (기간: {{기간}}, 출처: {{원문 문장}})
(원문에 수치가 없으면 "없음"이라고 표기)

## 언급된 도구·서비스
- {{도구}}: {{용도 - 원문에서 어떻게 쓰였는지}}
(언급 없으면 "없음")

## 언급된 다른 creator·앱
- {{이름}}: {{맥락}}
(언급 없으면 "없음")

## 복제 가능한 전술 (≤3)
1. {{전술 - 운영자가 바로 실행 가능한 수준으로 구체화}}
   - 구체적 스텝: {{단계별 행동}}
   - 예상 리소스: {{시간/비용/도구}}
   - 예상 효과: {{원문 기반 기대 결과}}
(전술이 없으면 "없음")

## 원문 요약 (≤5문장)
{{요약}}

## 본문 포인트별 발췌
> {{원문에서 뽑은 주요 문장 1}} (원문 변형 금지)
> {{원문에서 뽑은 주요 문장 2}}
> {{원문에서 뽑은 주요 문장 3}}
(최대 5개 인용)

이 템플릿을 그대로 {output_path}에 write하세요. 설명 없이 파일만 생성."""


def collect_blog_files(creator_dir: Path) -> list[Path]:
    """
    Blog/{creator}/ 하위 카테고리 폴더의 모든 .md 파일 수집.
    insights/ 폴더와 uncategorized/ 는 제외.
    """
    excluded = {"insights", "uncategorized"}
    result = []
    for cat_dir in sorted(creator_dir.iterdir()):
        if not cat_dir.is_dir():
            continue
        if cat_dir.name in excluded:
            continue
        result.extend(sorted(cat_dir.glob("*.md")))
    return result


def parse_frontmatter(content: str) -> dict:
    """파일 내용에서 frontmatter 키-값 추출 (간단 파싱)."""
    import re
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1]
    result = {}
    for line in fm_text.splitlines():
        m = re.match(r'^(\w[\w_]*):\s*(.+)$', line)
        if m:
            key, val = m.group(1), m.group(2).strip().strip('"\'')
            result[key] = val
    return result


def extract_insight_for_post(
    post_path: Path,
    insights_dir: Path,
    creator: str,
    codex: str,
    skip_existing: bool,
) -> bool:
    """
    단일 블로그 포스트 파일에서 구조화 인사이트 추출.
    성공 시 True, codex 실패/skip 시 False 반환.
    파일 삭제는 절대 하지 않음.
    """
    slug = post_path.stem
    output_path = insights_dir / f"{slug}-insight.md"

    if skip_existing and output_path.exists():
        print(f"  [skip] {slug}-insight.md 이미 존재")
        return True

    # 입력 파일 내용 읽기
    try:
        content = post_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [error] {post_path.name} 읽기 실패: {e}")
        return False

    # frontmatter 메타데이터 추출
    fm = parse_frontmatter(content)
    url = fm.get("url") or fm.get("source") or fm.get("canonical_url") or ""
    title = fm.get("title") or slug
    published_at = fm.get("published_at") or ""
    collected_at = fm.get("collected_at") or ""
    categories_raw = fm.get("categories") or ""
    today = date.today().isoformat()

    # 임시 입력 파일 (codex가 읽을 원본 포스트)
    tmp_input = f"/tmp/tc_blog_insight_in_{slug[:40]}.md"
    try:
        import shutil
        shutil.copy2(str(post_path), tmp_input)
    except Exception as e:
        print(f"  [error] 임시 파일 복사 실패: {e}")
        return False

    output_path_str = str(output_path)
    prompt = EXTRACT_PROMPT_TEMPLATE.format(
        input_path=tmp_input,
        output_path=output_path_str,
        creator=creator,
        url=url,
        title=title,
        published_at=published_at,
        collected_at=collected_at,
        categories=categories_raw,
        today=today,
    )

    # stale 출력 제거
    if output_path.exists():
        output_path.unlink()

    proc = None
    try:
        proc = subprocess.run(
            [codex, "exec", "--full-auto", "--ephemeral",
             "--model", "gpt-5.4",
             "--add-dir", "/tmp",
             "-C", str(insights_dir.parent),  # creator 디렉토리를 workspace로
             prompt],
            capture_output=True, text=True, timeout=300,
        )
    except subprocess.TimeoutExpired:
        print(f"  [timeout] {slug}")
        return False
    except Exception as e:
        print(f"  [error] codex 실행 실패: {e}")
        return False

    if output_path.exists() and output_path.stat().st_size > 100:
        print(f"  [ok] {slug}-insight.md ({output_path.stat().st_size:,} bytes)")
        return True
    else:
        # codex가 결과를 쓰지 않음 — 원본 포스트 파일은 절대 건드리지 않음
        print(f"  [fail] {slug} — codex 결과 없음")
        if proc and proc.stderr:
            tail = "\n".join(proc.stderr.strip().splitlines()[-3:])
            if tail:
                print(f"    stderr: {tail}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="블로그 글 1개당 구조화 인사이트 추출 (codex exec)."
    )
    parser.add_argument("--creator", required=True,
                        help="Creator slug, 예: programmingzombie")
    parser.add_argument("--slug", default=None,
                        help="특정 파일 slug만 처리 (예: 2024-12-01-foo)")
    parser.add_argument("--skip-existing", action="store_true",
                        help="이미 insight 파일이 있는 경우 건너뜀")
    parser.add_argument("--blog-dir", dest="blog_dir", default=None,
                        help="Blog/ 루트 경로 (기본: repo 루트의 Blog/)")
    args = parser.parse_args()

    blog_root = Path(args.blog_dir) if args.blog_dir else Path.cwd() / "Blog"
    creator_dir = blog_root / args.creator

    if not creator_dir.exists():
        sys.exit(f"Blog/{args.creator}/ 없음 — 수집 먼저 실행")

    codex = find_codex()
    if not codex:
        sys.exit("ERROR: codex not found. Install via: npm install -g @openai/codex")

    insights_dir = creator_dir / "insights"
    insights_dir.mkdir(parents=True, exist_ok=True)

    # 대상 파일 수집
    if args.slug:
        # 특정 slug 지정 시 전체 creator_dir에서 파일 탐색
        candidates = list(creator_dir.rglob(f"{args.slug}.md"))
        candidates = [f for f in candidates if "insights" not in f.parts]
        if not candidates:
            sys.exit(f"Blog/{args.creator}/**/{args.slug}.md 없음")
        target_files = candidates[:1]
    else:
        target_files = collect_blog_files(creator_dir)

    if not target_files:
        sys.exit(f"Blog/{args.creator}/ 에 분류된 블로그 글 없음 — /classify 먼저 실행")

    print(f"ExtractInsights — {args.creator}")
    print(f"  대상: {len(target_files)} 파일")
    print(f"  출력: Blog/{args.creator}/insights/{{slug}}-insight.md")
    print()

    success = 0
    fail = 0
    skipped_count = 0

    for post_path in target_files:
        slug = post_path.stem
        output_path = insights_dir / f"{slug}-insight.md"

        if args.skip_existing and output_path.exists():
            skipped_count += 1
            continue

        ok = extract_insight_for_post(
            post_path, insights_dir, args.creator, codex, skip_existing=False
        )
        if ok:
            success += 1
        else:
            fail += 1

    print()
    print(f"ExtractInsights 완료 — {args.creator}")
    print(f"  성공: {success}")
    if fail:
        print(f"  실패 (원본 보존): {fail}")
    if skipped_count:
        print(f"  Skip (이미 존재): {skipped_count}")

    # 생성된 인사이트 파일 목록
    created = sorted(f.name for f in insights_dir.glob("*-insight.md"))
    if created:
        print(f"\n  생성된 인사이트 파일:")
        for name in created:
            size = (insights_dir / name).stat().st_size
            print(f"    {name}  ({size:,} bytes)")


if __name__ == "__main__":
    main()
