"""블로그 수집 adapter 모음.

get_adapter(url, hint) 팩토리 함수로 적절한 adapter를 선택한다.
"""
from __future__ import annotations

from urllib.parse import urlparse

from sources.blog.collect import BlogAdapter
from sources.blog.adapters.rss import RssAdapter
from sources.blog.adapters.sitemap import SitemapAdapter
from sources.blog.adapters.tistory import TistoryAdapter
from sources.blog.adapters.generic_html import GenericHtmlAdapter


def get_adapter(root_url: str, hint: str | None = None) -> BlogAdapter:
    """targets.yaml의 adapter 힌트 또는 URL 도메인을 보고 적절한 adapter를 선택한다.

    hint = 'auto' | 'rss' | 'sitemap' | 'tistory' | 'medium' | 'substack' | 'generic_html'
    auto인 경우: tistory 도메인이면 Tistory, 그 외는 RSS 시도 기본.
    """
    host = urlparse(root_url).netloc.lower()

    if hint == "tistory" or host.endswith(".tistory.com"):
        return TistoryAdapter()
    if hint == "rss":
        return RssAdapter()
    if hint == "sitemap":
        return SitemapAdapter()
    if hint == "generic_html":
        return GenericHtmlAdapter()
    # substack은 /feed 경로 RSS
    if hint == "substack" or "substack.com" in host:
        return RssAdapter()
    # medium도 /feed RSS
    if hint == "medium" or "medium.com" in host:
        return RssAdapter()

    # auto: RSS 시도가 기본
    return RssAdapter()


__all__ = [
    "get_adapter",
    "RssAdapter",
    "SitemapAdapter",
    "TistoryAdapter",
    "GenericHtmlAdapter",
]
