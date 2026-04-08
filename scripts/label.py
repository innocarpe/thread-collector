#!/usr/bin/env python3
"""
ThreadCollector — AI auto-labeler
Uses Claude API (haiku) to assign topic labels to collected posts.

Usage:
  python3 scripts/label.py                        # label all unlabeled posts
  python3 scripts/label.py --all                  # re-label everything
  python3 scripts/label.py --user dalgom.bami     # specific user only
  python3 scripts/label.py --file path/to/post.md # single file

Requires: ANTHROPIC_API_KEY in .env.local or environment.
Install:  pip install anthropic
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# ── Label taxonomy ─────────────────────────────────────────────────────────────

LABELS: list[str] = [
    # 빌딩/개발
    "앱개발",       # iOS, Android, 모바일 앱 개발 및 출시
    "웹/SaaS",      # 웹 서비스, SaaS 제품 개발
    "AI/LLM",       # AI 기능 개발, 프롬프트 엔지니어링, LLM 활용
    "개발도구",     # 개발 환경, 도구, 프레임워크, 기술 스택
    # 마케팅/성장
    "마케팅",       # 마케팅 채널, 광고, 홍보 전략
    "바이럴/SNS",   # 바이럴 성장, SNS 콘텐츠 마케팅
    "ASO/검색",     # ASO, SEO, 키워드 전략, 검색 최적화
    "수익화",       # 가격 전략, 수익 모델, 매출, 수익성
    "성장전략",     # 사용자 획득, 리텐션, 성장 지표, 그로스해킹
    # 스타트업/제품
    "인디해킹",     # 인디 해커, 솔로 창업자, 소규모 제품
    "PMF",          # 제품-시장 적합성, 고객 검증
    "제품전략",     # 로드맵, 기능 결정, 제품 방향성
    "MVP/런칭",     # MVP, 초기 출시, 빠른 검증
    "스타트업",     # 스타트업 전략, 투자, 팀빌딩
    # 커리어/마인드
    "창업철학",     # 창업 마인드셋, 철학, 태도
    "개발자커리어", # 개발자 커리어, 취업, 이직, 성장
    "생산성",       # 생산성, 워크플로우, 루틴, 시간관리
    "학습/스킬",    # 학습법, 스킬 개발, 자기계발
    "회고/인사이트",# 회고, 실패 경험, 배움, 사례 분석
]

LABEL_SET = set(LABELS)

BATCH_SIZE = 10  # posts per API call

SYSTEM_PROMPT = f"""당신은 한국 스타트업/개발자 커뮤니티의 Threads 게시글을 분류하는 전문가입니다.

다음 레이블 목록에서 각 게시글에 가장 적합한 1~3개의 레이블을 선택하세요:
{json.dumps(LABELS, ensure_ascii=False, indent=2)}

레이블 선택 기준:
- "앱개발": iOS/Android/Flutter/React Native 앱 개발, 앱 스토어 관련
- "웹/SaaS": 웹 서비스, SaaS, 웹앱 개발
- "AI/LLM": AI 도구 활용, LLM, ChatGPT/Claude, 프롬프트 엔지니어링
- "개발도구": IDE, 라이브러리, 프레임워크, 기술 스택 선택, 인프라
- "마케팅": 마케팅 전략, 광고 채널, 브랜딩
- "바이럴/SNS": SNS 콘텐츠, 바이럴 마케팅, 인플루언서
- "ASO/검색": 앱스토어 최적화, SEO, 키워드 리서치
- "수익화": 수익 모델, 가격 책정, 매출, 광고 수익
- "성장전략": 그로스해킹, 사용자 획득, 리텐션, KPI
- "인디해킹": 솔로 창업, 사이드프로젝트, 소규모 운영
- "PMF": 제품-시장 적합성, 고객 인터뷰, 검증
- "제품전략": 로드맵, 기능 우선순위, 제품 결정
- "MVP/런칭": 출시 전략, MVP, 프로덕트헌트, 베타 테스트
- "스타트업": 스타트업 운영, 투자 유치, 팀, 조직 문화
- "창업철학": 창업가 마인드셋, 삶의 철학, 관점
- "개발자커리어": 개발자 성장, 이직, 연봉, 직장 생활
- "생산성": 효율적 업무 방식, 도구, 루틴, 집중
- "학습/스킬": 새 기술 습득, 공부법, 성장 방법
- "회고/인사이트": 경험 정리, 실패 사례, 배운 점

입력 형식: JSON 배열 (pk와 본문 포함)
출력 형식: JSON 객체, 키는 pk(문자열), 값은 레이블 배열
예시: {{"3612345678": ["마케팅", "수익화"], "3698765432": ["앱개발", "MVP/런칭"]}}
반드시 JSON만 출력하고 다른 텍스트는 포함하지 마세요."""

# ── Frontmatter utilities ──────────────────────────────────────────────────────

def read_frontmatter_and_content(path: Path) -> tuple[dict, str, str]:
    """Returns (frontmatter_dict, raw_frontmatter_block, body)"""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}, "", raw

    end = raw.find("---", 3)
    if end == -1:
        return {}, "", raw

    fm_block = raw[3:end].strip()
    body = raw[end + 3:].lstrip("\n")

    fm: dict = {}
    for line in fm_block.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")

    return fm, raw[:end + 3], body


def write_labels_to_file(path: Path, labels: list[str]) -> None:
    """Adds or replaces the `labels` field in a file's YAML frontmatter."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return

    end = raw.find("---", 3)
    if end == -1:
        return

    fm_block = raw[3:end]
    body = raw[end + 3:]

    # Remove existing labels line if present
    fm_lines = [l for l in fm_block.split("\n") if not l.strip().startswith("labels:")]

    # Build labels YAML
    labels_yaml = "labels: [" + ", ".join(f'"{l}"' for l in labels) + "]"
    fm_lines.append(labels_yaml)

    new_raw = "---" + "\n".join(fm_lines) + "---" + body
    path.write_text(new_raw, encoding="utf-8")


def has_labels(path: Path) -> bool:
    """Returns True if the file already has a non-empty labels field."""
    try:
        fm, _, _ = read_frontmatter_and_content(path)
        labels_raw = fm.get("labels", "").strip()
        return bool(labels_raw and labels_raw != "[]")
    except Exception:
        return False

# ── Claude API ────────────────────────────────────────────────────────────────

def get_client():
    """Return an Anthropic client, loading ANTHROPIC_API_KEY from env or .env.local."""
    try:
        import anthropic  # type: ignore
    except ImportError:
        sys.exit(
            "ERROR: anthropic package not found.\n"
            "Install with: pip install anthropic"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Try loading from .env.local
        env_path = Path(__file__).parent.parent / ".env.local"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"')
                    break

    if not api_key:
        sys.exit(
            "ERROR: ANTHROPIC_API_KEY not found.\n"
            "Add it to .env.local:\n"
            "  ANTHROPIC_API_KEY=sk-ant-..."
        )

    return anthropic.Anthropic(api_key=api_key)


def label_batch(client, posts: list[dict]) -> dict[str, list[str]]:
    """
    Send a batch of posts to Claude and return {pk: [labels]} mapping.
    posts: [{"pk": "...", "text": "..."}]
    """
    payload = [{"pk": p["pk"], "text": p["text"][:600]} for p in posts]
    prompt = json.dumps(payload, ensure_ascii=False)

    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text.strip()

        # Extract JSON if wrapped in markdown code block
        if raw.startswith("```"):
            raw = re.sub(r"^```[a-z]*\n?", "", raw)
            raw = re.sub(r"\n?```$", "", raw)

        result = json.loads(raw)

        # Validate — only keep known labels
        validated: dict[str, list[str]] = {}
        for pk, lbls in result.items():
            if isinstance(lbls, list):
                validated[str(pk)] = [l for l in lbls if l in LABEL_SET]
        return validated

    except Exception as e:
        print(f"  [warn] batch failed: {e}", file=sys.stderr)
        return {}


# ── Main labeling logic ────────────────────────────────────────────────────────

def collect_files(root: Path, user: str | None = None) -> list[Path]:
    """Collect all markdown files under Threads/."""
    if not root.exists():
        return []

    pattern = f"{user}/**/*.md" if user else "**/*.md"
    return sorted(root.glob(pattern))


def label_files(files: list[Path], client, force: bool = False, verbose: bool = True) -> int:
    """
    Label a list of markdown files.
    Returns the number of files that were updated.
    """
    to_label: list[Path] = []
    for f in files:
        if force or not has_labels(f):
            to_label.append(f)

    if not to_label:
        if verbose:
            print("  모든 파일에 이미 레이블이 있습니다.")
        return 0

    if verbose:
        print(f"  {len(to_label)}개 파일 레이블링 예정 (전체 {len(files)}개 중)")

    # Build post objects from files
    posts_map: dict[str, dict] = {}
    for f in to_label:
        fm, _, body = read_frontmatter_and_content(f)
        pk = fm.get("pk", "").strip('"')
        if not pk:
            continue
        # Combine title line + body for better classification
        text = body.replace("# ", "", 1).strip()
        posts_map[pk] = {"pk": pk, "text": text, "path": f}

    posts_list = list(posts_map.values())
    batches = [posts_list[i:i + BATCH_SIZE] for i in range(0, len(posts_list), BATCH_SIZE)]

    updated = 0
    for i, batch in enumerate(batches):
        if verbose:
            pct = int((i / len(batches)) * 100)
            pks_preview = [p["pk"][:8] for p in batch[:3]]
            print(f"  배치 {i + 1}/{len(batches)} ({pct}%) — {len(batch)}개 처리 중...")

        result = label_batch(client, batch)

        for post in batch:
            pk = post["pk"]
            labels = result.get(pk, [])
            if labels:
                write_labels_to_file(post["path"], labels)
                updated += 1
            elif verbose:
                print(f"    [skip] {pk}: 레이블 없음")

        # Rate limiting: small sleep between batches
        if i < len(batches) - 1:
            time.sleep(0.3)

    return updated


def label_single_file(file_path: Path, force: bool = False) -> list[str]:
    """
    Label a single file. Returns the assigned labels (empty list on skip/fail).
    This is the function imported by collect.py.
    """
    if not force and has_labels(file_path):
        fm, _, _ = read_frontmatter_and_content(file_path)
        raw = fm.get("labels", "[]")
        return json.loads(raw.replace("'", '"')) if raw != "[]" else []

    client = get_client()
    fm, _, body = read_frontmatter_and_content(file_path)
    pk = fm.get("pk", "").strip('"')
    if not pk:
        return []

    text = body.replace("# ", "", 1).strip()
    result = label_batch(client, [{"pk": pk, "text": text}])
    labels = result.get(pk, [])
    if labels:
        write_labels_to_file(file_path, labels)
    return labels


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Auto-label ThreadCollector posts using Claude AI.")
    p.add_argument("--all", action="store_true", help="Re-label all posts, including already-labeled ones.")
    p.add_argument("--user", default=None, help="Only label posts from this user (e.g. dalgom.bami).")
    p.add_argument("--file", default=None, help="Label a single markdown file.")
    p.add_argument(
        "--threads-dir",
        dest="threads_dir",
        default=None,
        help="Root directory of collected posts (default: Threads/ relative to CWD).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    threads_root = Path(args.threads_dir) if args.threads_dir else Path.cwd() / "Threads"

    print("ThreadCollector Labeler")
    print(f"  모델  : claude-haiku-4-5-20251001")
    print(f"  레이블: {len(LABELS)}개 정의됨")
    print()

    client = get_client()

    if args.file:
        path = Path(args.file)
        if not path.exists():
            sys.exit(f"ERROR: 파일을 찾을 수 없습니다: {path}")
        labels = label_single_file(path, force=args.all)
        print(f"  결과: {labels}")
        return

    files = collect_files(threads_root, user=args.user)
    if not files:
        sys.exit(f"ERROR: 마크다운 파일 없음 ({threads_root})")

    print(f"  대상 : {threads_root}" + (f" / @{args.user}" if args.user else ""))
    print(f"  전체 : {len(files)}개 파일")
    print()

    updated = label_files(files, client, force=args.all)

    print()
    print(f"완료: {updated}개 파일 레이블링됨")


if __name__ == "__main__":
    main()
