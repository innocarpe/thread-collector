"""블로그 수집 entry point (Phase 1 스켈레톤).

실제 fetch/parse 로직은 Phase 2A에서 sources/blog/adapters/ 에 구현.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


@dataclass
class PostRef:
    """Adapter가 discover 단계에서 반환하는 글 레퍼런스."""
    url: str
    title: str | None = None
    published_at: str | None = None  # ISO 8601
    canonical_url: str | None = None


@dataclass
class Post:
    """fetch 결과 — 본문 포함."""
    url: str
    canonical_url: str
    title: str
    published_at: str | None
    author: str | None
    content_markdown: str
    raw_html: str | None = None
    lang: str | None = None
    extras: dict = field(default_factory=dict)


class BlogAdapter(Protocol):
    """모든 블로그 adapter가 구현해야 할 최소 계약."""

    name: str

    def discover_posts(self, root_url: str) -> list[PostRef]:
        """피드·sitemap·HTML을 파싱해 글 목록을 반환."""
        ...

    def fetch_post(self, post_ref: PostRef) -> Post:
        """개별 글의 본문과 메타데이터를 가져온다."""
        ...

    def detect_language(self, post: Post) -> str:
        """글의 언어 감지 (ko, en 등)."""
        ...


def main() -> int:
    raise NotImplementedError(
        "sources/blog/collect.py 는 Phase 1 스켈레톤입니다. "
        "Phase 2A에서 adapters/rss.py, sitemap.py, tistory.py, generic_html.py를 "
        "구현한 뒤 이 함수를 완성하세요."
    )


if __name__ == "__main__":
    sys.exit(main())
