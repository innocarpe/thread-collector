"""블로그 포스트 저장 + dedup 관리.

저장 경로: Blog/{creator_slug}/{category_or_uncategorized}/{YYYY-MM-DD}-{slug}.md
dedup 인덱스: Blog/{creator_slug}/.index.jsonl
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from sources.blog.collect import Post


# ────────────────────────────────────────────────────────────────────────────
# 내부 헬퍼
# ────────────────────────────────────────────────────────────────────────────

def _slugify(text: str, max_len: int = 60) -> str:
    """텍스트를 URL-safe slug로 변환."""
    # 유니코드 정규화
    text = unicodedata.normalize("NFKD", text)
    # 한글·영문·숫자·공백·하이픈만 유지
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    text = text.lower().strip("-")
    return text[:max_len] if text else "post"


def _derive_slug_from_url(url: str) -> str:
    """URL 마지막 path segment에서 slug를 유도."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    last = path.split("/")[-1] if path else ""
    # 숫자만으로 된 경우 (Tistory 스타일) 그대로 사용
    if last:
        return _slugify(last) or last
    return _slugify(url)


def _format_frontmatter(creator_slug: str, post: Post, category: str) -> str:
    """YAML frontmatter 문자열을 생성."""
    canonical = post.canonical_url or post.url
    published = post.published_at or ""
    collected = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    author = post.author or ""
    lang = post.lang or "ko"
    word_count = len(post.content_markdown.split())
    adapter_name = post.extras.get("adapter", "unknown")

    lines = [
        "---",
        "source: blog",
        f"creator: {creator_slug}",
        f"url: {canonical}",
        f"title: {_yaml_str(post.title)}",
        f"published_at: {published}",
        f"collected_at: {collected}",
        f"author: {_yaml_str(author)}",
        f"lang: {lang}",
        "categories: []",
        "extras:",
        f"  word_count: {word_count}",
        f"  adapter: {adapter_name}",
        "---",
        "",
    ]
    return "\n".join(lines)


def _yaml_str(s: str) -> str:
    """YAML 단일값 문자열 이스케이프 (간이)."""
    if not s:
        return '""'
    # 특수문자가 있으면 따옴표로 감쌈
    if any(c in s for c in ('"', "'", ":", "#", "\n", "{")):
        escaped = s.replace('"', '\\"')
        return f'"{escaped}"'
    return s


# ────────────────────────────────────────────────────────────────────────────
# dedup 인덱스
# ────────────────────────────────────────────────────────────────────────────

def _index_path(creator_slug: str, output_root: Path) -> Path:
    return output_root / creator_slug / ".index.jsonl"


def _load_index(creator_slug: str, output_root: Path) -> set[str]:
    """이미 수집된 canonical URL 집합을 반환."""
    index_file = _index_path(creator_slug, output_root)
    if not index_file.exists():
        return set()
    collected: set[str] = set()
    for line in index_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            url = entry.get("canonical_url", "")
            if url:
                collected.add(url)
        except json.JSONDecodeError:
            pass
    return collected


def already_collected(
    creator_slug: str,
    canonical_url: str,
    output_root: Path = Path("Blog"),
) -> bool:
    """해당 URL이 이미 수집됐는지 확인."""
    return canonical_url in _load_index(creator_slug, output_root)


def mark_collected(
    creator_slug: str,
    canonical_url: str,
    slug: str,
    output_root: Path = Path("Blog"),
) -> None:
    """수집 완료 URL을 인덱스에 기록."""
    index_file = _index_path(creator_slug, output_root)
    index_file.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "canonical_url": canonical_url,
        "slug": slug,
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }
    with index_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ────────────────────────────────────────────────────────────────────────────
# 저장
# ────────────────────────────────────────────────────────────────────────────

def save_post(
    creator_slug: str,
    post: Post,
    category: str = "uncategorized",
    output_root: Path = Path("Blog"),
) -> Path:
    """Post를 마크다운 파일로 저장하고 인덱스를 갱신한다.

    Returns:
        저장된 파일 경로
    """
    canonical = post.canonical_url or post.url

    # 파일명: {YYYY-MM-DD}-{slug}.md
    date_prefix = (post.published_at or "0000-00-00")[:10]
    url_slug = _derive_slug_from_url(canonical)
    filename = f"{date_prefix}-{url_slug}.md"

    dest_dir = output_root / creator_slug / category
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filename

    frontmatter = _format_frontmatter(creator_slug, post, category)
    content = frontmatter + "\n" + post.content_markdown

    dest_path.write_text(content, encoding="utf-8")

    # dedup 인덱스 갱신
    mark_collected(creator_slug, canonical, url_slug, output_root)

    return dest_path


# ────────────────────────────────────────────────────────────────────────────
# 인덱스 재구축
# ────────────────────────────────────────────────────────────────────────────

# insights/ 폴더는 포스트가 아니므로 제외
_EXCLUDE_DIRS = {"insights"}


def _parse_frontmatter_url(md_path: Path) -> str | None:
    """마크다운 파일 frontmatter에서 url 필드를 추출 (표준 라이브러리만 사용)."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError:
        return None

    # frontmatter 블록 추출: --- 로 시작하고 두 번째 --- 까지
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm_block = text[3:end]

    # url: <value> 패턴 탐색 (간이 파서 — PyYAML 미사용)
    for line in fm_block.splitlines():
        m = re.match(r"^url:\s*(.+)", line)
        if m:
            value = m.group(1).strip()
            # 따옴표 제거
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            return value if value else None
    return None


def rebuild_index(
    creator_slug: str,
    output_root: Path = Path("Blog"),
) -> dict[str, int]:
    """디스크 파일시스템 truth 기반으로 .index.jsonl 을 재구축한다.

    - insights/ 폴더 제외, 그 외 모든 카테고리 폴더의 *.md 파일 스캔
    - 각 파일 frontmatter의 url 필드로 canonical_url 결정
    - 동일 canonical_url 중복 시 가장 최신 slug(파일명)를 보존
    - 기존 인덱스는 .index.jsonl.bak 으로 백업
    - 임시 파일 → 원자적 교체(os.replace)

    Returns:
        {"before": 기존행수, "after": 새행수, "files": 스캔파일수}
    """
    creator_dir = output_root / creator_slug
    index_file = _index_path(creator_slug, output_root)

    # ── 기존 행수 기록 ──────────────────────────────────────────────────────
    before_lines = 0
    if index_file.exists():
        before_lines = sum(1 for l in index_file.read_text(encoding="utf-8").splitlines() if l.strip())

    # ── 디스크에서 .md 스캔 ──────────────────────────────────────────────────
    # url → (slug, md_path)  중복 시 파일명(날짜 포함) 사전순 마지막 우선
    url_to_info: dict[str, tuple[str, Path]] = {}
    scanned = 0

    for category_dir in sorted(creator_dir.iterdir()):
        if not category_dir.is_dir():
            continue
        if category_dir.name in _EXCLUDE_DIRS or category_dir.name.startswith("."):
            continue
        for md_path in sorted(category_dir.glob("*.md")):
            scanned += 1
            url = _parse_frontmatter_url(md_path)
            if not url:
                # frontmatter에 url 없으면 파일명에서 slug 유도
                url = md_path.stem  # fallback: 최소한 중복은 막음
            slug = _derive_slug_from_url(url)
            # 같은 url이 이미 있으면 파일명 사전순 마지막을 선호
            if url not in url_to_info or md_path.name > url_to_info[url][1].name:
                url_to_info[url] = (slug, md_path)

    # ── 새 인덱스 작성 (임시 파일) ──────────────────────────────────────────
    tmp_path = index_file.with_suffix(".jsonl.tmp")
    now = datetime.now(timezone.utc).isoformat()
    with tmp_path.open("w", encoding="utf-8") as f:
        for canonical_url, (slug, _) in sorted(url_to_info.items()):
            entry = {
                "canonical_url": canonical_url,
                "slug": slug,
                "collected_at": now,
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ── 백업 + 원자적 교체 ──────────────────────────────────────────────────
    if index_file.exists():
        bak_path = index_file.with_suffix(".jsonl.bak")
        os.replace(index_file, bak_path)

    os.replace(tmp_path, index_file)

    after_lines = len(url_to_info)
    return {"before": before_lines, "after": after_lines, "files": scanned}


# ────────────────────────────────────────────────────────────────────────────
# CLI 진입점
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Blog/.index.jsonl 유틸리티",
    )
    parser.add_argument(
        "--rebuild-index",
        metavar="CREATOR_SLUG",
        help="디스크 파일 기반으로 .index.jsonl 을 재구축 (예: programmingzombie)",
    )
    parser.add_argument(
        "--output-root",
        default="Blog",
        help="Blog 루트 디렉터리 (기본값: Blog)",
    )
    args = parser.parse_args()

    if args.rebuild_index:
        root = Path(args.output_root)
        print(f"[rebuild_index] creator={args.rebuild_index!r}, root={root}")
        stats = rebuild_index(args.rebuild_index, output_root=root)
        print(f"  정리 전  행수: {stats['before']}")
        print(f"  스캔 파일: {stats['files']}")
        print(f"  정리 후  행수: {stats['after']}")
        delta = stats["before"] - stats["after"]
        print(f"  제거된 중복/고아: {delta}")
        bak = root / args.rebuild_index / ".index.jsonl.bak"
        if bak.exists():
            print(f"  백업: {bak}")
    else:
        parser.print_help()
        sys.exit(1)
