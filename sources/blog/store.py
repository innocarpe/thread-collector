"""블로그 포스트 저장 + dedup 관리.

저장 경로: Blog/{creator_slug}/{category_or_uncategorized}/{YYYY-MM-DD}-{slug}.md
dedup 인덱스: Blog/{creator_slug}/.index.jsonl
"""
from __future__ import annotations

import json
import re
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
