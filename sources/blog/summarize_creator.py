#!/usr/bin/env python3
"""
ThreadCollector — creator 전체 종합 인사이트 생성
Usage: python3 -m sources.blog.summarize_creator --creator programmingzombie
       python3 -m sources.blog.summarize_creator --creator programmingzombie --only overview,playbook

모든 Blog/{creator}/insights/*-insight.md 를 모아 4개 요약 파일 생성:
  1. overview.md         — creator 개요
  2. patterns.md         — 반복되는 패턴·전술·도구
  3. key-posts.md        — 인사이트 밀도 높은 Top 10 글
  4. replication-playbook.md — TemperStone 복제 플레이북 (Day1/Week1/Month1)

Notes:
- codex None 응답 시 파일 삭제/수정 금지 — skip 후 재시도
- 인사이트 파일이 0개면 extract_insights 먼저 실행하도록 안내
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

# repo 루트를 sys.path에 추가
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sources._common.codex import find_codex

# 생성할 요약 파일 정의
SUMMARY_FILES = ["overview", "patterns", "key-posts", "replication-playbook"]


def build_overview_prompt(creator: str, insights_dir: Path, insight_files: list[Path]) -> str:
    """overview.md 생성 프롬프트."""
    file_list = "\n".join(f"- {f.name}" for f in insight_files[:50])
    output_path = str(insights_dir / "overview.md")
    return (
        f"당신은 인디 개발자 분석 리서처입니다. creator '{creator}'의 블로그 인사이트 파일들을 읽고 "
        f"overview.md를 생성하세요.\n\n"
        f"읽어야 할 인사이트 파일들 ({len(insight_files)}개):\n{file_list}\n\n"
        f"각 파일은 Blog/{creator}/insights/ 디렉토리에 있습니다.\n\n"
        f"생성할 파일: {output_path}\n\n"
        "overview.md 내용 구성:\n"
        "# {creator} 블로그 인사이트 개요\n\n"
        "## 기본 정보\n"
        "- 총 글 수, 분석 기간, 주요 카테고리 분포\n\n"
        "## 핵심 주제 Top 5\n"
        "1. {주제}: {설명} — 글 수, 대표 제목 포함\n\n"
        "## creator 특성\n"
        "- 글쓰기 스타일, 주요 관심사, 반복 키워드\n\n"
        "## 주목할 만한 인사이트\n"
        "- 가장 임팩트 있는 주장·전술 3~5개 (파일 출처 명시)\n\n"
        "300~500 단어, 한국어로 작성. 파일만 생성, 설명 없음."
    )


def build_patterns_prompt(creator: str, insights_dir: Path, insight_files: list[Path]) -> str:
    """patterns.md 생성 프롬프트."""
    file_list = "\n".join(f"- {f.name}" for f in insight_files[:50])
    output_path = str(insights_dir / "patterns.md")
    return (
        f"당신은 인디 개발자 분석 리서처입니다. creator '{creator}'의 블로그 인사이트 파일들을 읽고 "
        f"patterns.md를 생성하세요.\n\n"
        f"읽어야 할 인사이트 파일들 ({len(insight_files)}개):\n{file_list}\n\n"
        f"각 파일은 Blog/{creator}/insights/ 디렉토리에 있습니다.\n\n"
        f"생성할 파일: {output_path}\n\n"
        "patterns.md 내용 구성:\n"
        "# {creator} 반복 패턴 분석\n\n"
        "## 반복 사용 전술\n"
        "- {전술명}: {설명} — 몇 번 등장했는지, 구체 방법\n\n"
        "## 일관되게 사용하는 도구\n"
        "- {도구}: {용도} — 여러 글에서 어떻게 쓰이는지\n\n"
        "## 반복되는 수익화 패턴\n"
        "- {패턴}: {설명} — 실제 수치가 있으면 포함\n\n"
        "## 핵심 믿음·철학\n"
        "- creator가 일관되게 주장하는 마인드셋·프레임워크\n"
        "- 실제 인용구 포함 (원문 변형 금지)\n\n"
        "## 성장 궤적\n"
        "- 시간 흐름에 따른 주제 변화, 전략 피봇, 스킬 발전\n\n"
        "400~600 단어, 한국어로 작성. 파일만 생성, 설명 없음."
    )


def build_key_posts_prompt(creator: str, insights_dir: Path, insight_files: list[Path]) -> str:
    """key-posts.md 생성 프롬프트."""
    file_list = "\n".join(f"- {f.name}" for f in insight_files[:50])
    output_path = str(insights_dir / "key-posts.md")
    return (
        f"당신은 인디 개발자 분석 리서처입니다. creator '{creator}'의 블로그 인사이트 파일들을 읽고 "
        f"key-posts.md를 생성하세요.\n\n"
        f"읽어야 할 인사이트 파일들 ({len(insight_files)}개):\n{file_list}\n\n"
        f"각 파일은 Blog/{creator}/insights/ 디렉토리에 있습니다.\n\n"
        f"생성할 파일: {output_path}\n\n"
        "key-posts.md 내용 구성:\n"
        "# {creator} 인사이트 핵심 글 Top 10\n\n"
        "인사이트 밀도(핵심 주장 수 + 공개 수치 + 복제 가능 전술)를 기준으로 Top 10 선정.\n\n"
        "각 글 형식:\n"
        "## {순위}. {글 제목}\n"
        "- **파일**: {slug}-insight.md\n"
        "- **URL**: {원문 URL}\n"
        "- **핵심 주장**: {1~3줄 요약}\n"
        "- **주목 이유**: {왜 이 글이 중요한지 1~2문장}\n\n"
        "테마별로 그룹핑 가능 (예: '수익화', 'AI 활용', '성장 전략' 등).\n"
        "한국어로 작성. 파일만 생성, 설명 없음."
    )


def build_playbook_prompt(creator: str, insights_dir: Path, insight_files: list[Path]) -> str:
    """replication-playbook.md 생성 프롬프트."""
    file_list = "\n".join(f"- {f.name}" for f in insight_files[:50])
    output_path = str(insights_dir / "replication-playbook.md")
    return (
        f"당신은 스타트업 전략 컨설턴트입니다. creator '{creator}'의 블로그 인사이트 파일들을 읽고 "
        f"'TemperStone이 이 creator의 전략을 복제하려면 무엇을 해야 하나?'를 "
        f"구체적인 실행 플레이북으로 작성하세요.\n\n"
        f"읽어야 할 인사이트 파일들 ({len(insight_files)}개):\n{file_list}\n\n"
        f"각 파일은 Blog/{creator}/insights/ 디렉토리에 있습니다.\n\n"
        f"생성할 파일: {output_path}\n\n"
        "replication-playbook.md 내용 구성:\n"
        f"# {creator} 전략 복제 플레이북\n\n"
        "## 복제할 핵심 전략 (Top 3)\n"
        "- {전략명}: {왜 복제 가능한지, 어떤 결과를 기대할 수 있는지}\n\n"
        "## Day 1 (오늘 당장)\n"
        "- [ ] {즉시 실행 가능한 구체적 액션}\n"
        "- 필요 도구: {목록}\n"
        "- 예상 소요 시간: {시간}\n\n"
        "## Week 1 (첫 주)\n"
        "- [ ] {이번 주 완료해야 할 태스크}\n"
        "- 우선순위 근거: {creator의 경험에서 도출}\n"
        "- 예상 결과: {지표 또는 산출물}\n\n"
        "## Month 1 (첫 달)\n"
        "- [ ] {한 달 목표}\n"
        "- 마일스톤: {중간 체크포인트}\n"
        "- 성공 지표: {측정 가능한 기준}\n\n"
        "## 주의사항 & 함정\n"
        "- creator가 실패했거나 경고한 것들 (있는 경우)\n"
        "- TemperStone 컨텍스트에서 주의할 점\n\n"
        "## 참고 글 (인사이트 출처)\n"
        "- {slug}-insight.md: {왜 이 글이 플레이북에 반영됐는지}\n\n"
        "원문에 없는 수치는 만들지 말 것. 실행 가능한 수준으로 구체화. 한국어로 작성. "
        "파일만 생성, 설명 없음."
    )


PROMPT_BUILDERS = {
    "overview": build_overview_prompt,
    "patterns": build_patterns_prompt,
    "key-posts": build_key_posts_prompt,
    "replication-playbook": build_playbook_prompt,
}


def run_codex_summary(
    creator: str,
    target_name: str,
    insights_dir: Path,
    insight_files: list[Path],
    codex: str,
) -> bool:
    """
    codex exec으로 단일 요약 파일 생성.
    성공 시 True, 실패 시 False (파일 삭제 안 함).
    """
    output_path = insights_dir / f"{target_name}.md"
    prompt_fn = PROMPT_BUILDERS[target_name]
    prompt = prompt_fn(creator, insights_dir, insight_files)

    # stale 파일 제거 (이전 실행 잔여물)
    if output_path.exists():
        output_path.unlink()

    proc = None
    try:
        proc = subprocess.run(
            [codex, "exec", "--full-auto", "--ephemeral",
             "--model", "gpt-5.4",
             "-s", "workspace-write",
             "-C", str(insights_dir),  # insights/ 를 workspace로
             prompt],
            capture_output=True, text=True, timeout=600,
        )
    except subprocess.TimeoutExpired:
        print(f"  [timeout] {target_name}.md 생성 실패 (600s 초과)")
        return False
    except Exception as e:
        print(f"  [error] {target_name}.md codex 실행 오류: {e}")
        return False

    if output_path.exists() and output_path.stat().st_size > 100:
        size = output_path.stat().st_size
        print(f"  [ok] {target_name}.md  ({size:,} bytes)")
        return True
    else:
        # codex가 결과를 쓰지 않음 — 기존 파일 절대 건드리지 않음
        print(f"  [fail] {target_name}.md — codex 결과 없음")
        if proc and proc.stderr:
            tail = "\n".join(proc.stderr.strip().splitlines()[-3:])
            if tail:
                print(f"    stderr: {tail}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="creator 전체 종합 인사이트 생성 (overview/patterns/key-posts/replication-playbook)."
    )
    parser.add_argument("--creator", required=True,
                        help="Creator slug, 예: programmingzombie")
    parser.add_argument(
        "--only",
        default=None,
        help="생성할 파일 선택 (콤마 구분). 예: overview,playbook\n"
             f"선택지: {', '.join(SUMMARY_FILES)}",
    )
    parser.add_argument("--blog-dir", dest="blog_dir", default=None,
                        help="Blog/ 루트 경로 (기본: repo 루트의 Blog/)")
    args = parser.parse_args()

    blog_root = Path(args.blog_dir) if args.blog_dir else Path.cwd() / "Blog"
    creator_dir = blog_root / args.creator
    insights_dir = creator_dir / "insights"

    if not creator_dir.exists():
        sys.exit(f"Blog/{args.creator}/ 없음 — 수집 먼저 실행")

    # 요청한 파일 목록 파싱
    if args.only:
        # "playbook" 단축어 → "replication-playbook"
        alias = {"playbook": "replication-playbook", "key_posts": "key-posts"}
        requested = []
        for item in args.only.split(","):
            item = item.strip()
            item = alias.get(item, item)
            if item not in SUMMARY_FILES:
                sys.exit(
                    f"알 수 없는 파일: '{item}'\n"
                    f"선택지: {', '.join(SUMMARY_FILES)}"
                )
            requested.append(item)
    else:
        requested = list(SUMMARY_FILES)

    codex = find_codex()
    if not codex:
        sys.exit("ERROR: codex not found. Install via: npm install -g @openai/codex")

    insights_dir.mkdir(parents=True, exist_ok=True)

    # 입력: extract_insights 로 생성된 *-insight.md 파일들
    insight_files = sorted(insights_dir.glob("*-insight.md"))
    if not insight_files:
        sys.exit(
            f"Blog/{args.creator}/insights/*-insight.md 없음\n"
            "extract_insights 먼저 실행하세요:\n"
            f"  python3 -m sources.blog.extract_insights --creator {args.creator}"
        )

    print(f"SummarizeCreator — {args.creator}")
    print(f"  인사이트 소스: {len(insight_files)} 파일")
    print(f"  생성할 파일: {', '.join(requested)}")
    print()

    success = 0
    fail = 0

    for target_name in requested:
        print(f"[{requested.index(target_name)+1}/{len(requested)}] {target_name}.md 생성 중...")
        ok = run_codex_summary(args.creator, target_name, insights_dir, insight_files, codex)
        if ok:
            success += 1
        else:
            fail += 1
        print()

    print(f"SummarizeCreator 완료 — {args.creator}")
    print(f"  성공: {success} / 시도: {len(requested)}")
    if fail:
        print(f"  실패: {fail} (codex 결과 없음 — 재실행 가능)")

    # 최종 파일 목록
    created_summaries = [insights_dir / f"{n}.md" for n in requested if (insights_dir / f"{n}.md").exists()]
    if created_summaries:
        print(f"\n  생성된 파일:")
        for f in created_summaries:
            print(f"    {f.relative_to(blog_root)}  ({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
