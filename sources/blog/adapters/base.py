"""BaseAdapter — BlogAdapter Protocol 공통 구현."""
from __future__ import annotations

import re

from sources.blog.collect import Post


class BaseAdapter:
    """BlogAdapter Protocol의 공통 로직을 제공하는 기반 클래스.

    detect_language는 여기서 구현하므로 서브클래스는 재정의 없이 사용 가능.
    """

    name: str = "base"

    # ────────────────────────────────────────────────────────────
    # 언어 감지
    # ────────────────────────────────────────────────────────────

    def detect_language(self, post: Post) -> str:
        """글의 언어를 감지한다.

        한글 문자 비율 > 30% 이면 'ko', 그 외 'en' 반환.
        """
        text = post.content_markdown or post.title or ""
        if not text:
            return "en"

        total_alpha = sum(1 for c in text if c.isalpha())
        if total_alpha == 0:
            return "en"

        korean_chars = sum(1 for c in text if "\uAC00" <= c <= "\uD7A3" or "\u1100" <= c <= "\u11FF")
        ratio = korean_chars / total_alpha

        return "ko" if ratio > 0.3 else "en"

    # ────────────────────────────────────────────────────────────
    # 공통 slug 유틸
    # ────────────────────────────────────────────────────────────

    @staticmethod
    def url_to_slug(url: str) -> str:
        """URL에서 간단한 식별 slug를 유도."""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")
        last = path.split("/")[-1] if path else ""
        slug = re.sub(r"[^\w-]", "-", last)
        slug = re.sub(r"-+", "-", slug).strip("-")
        return slug or "post"
