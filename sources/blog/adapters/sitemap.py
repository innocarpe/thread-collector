"""sitemap.xml 파서 adapter."""
from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse

from sources.blog.adapters.base import BaseAdapter
from sources.blog.collect import Post, PostRef
from sources.blog.fetch import can_fetch, fetch_text
from sources.blog.html_to_md import html_to_markdown

logger = logging.getLogger(__name__)

# sitemap XML 네임스페이스
_SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

# 포스트 URL 판별 패턴 (보수적)
_POST_URL_PATTERNS = [
    re.compile(r"/\d{4}/\d{2}/"),       # /2024/06/
    re.compile(r"/post[s]?/"),
    re.compile(r"/entry/"),
    re.compile(r"/blog/"),
    re.compile(r"/\d+$"),               # Tistory: /123
    re.compile(r"/\d+/?$"),
]

_MAX_URLS = 1000


def _looks_like_post(url: str) -> bool:
    """URL이 블로그 포스트처럼 보이는지 확인."""
    parsed = urlparse(url)
    # 쿼리스트링 있으면 제외
    if parsed.query:
        return False
    path = parsed.path
    # 루트 / 또는 짧은 경로 제외
    if len(path.strip("/")) < 3:
        return False
    for pattern in _POST_URL_PATTERNS:
        if pattern.search(path):
            return True
    return False


def _parse_sitemap_xml(xml_text: str, root_url: str) -> tuple[list[str], list[str]]:
    """sitemap XML을 파싱해 (하위 sitemap URL 목록, 포스트 URL 목록)을 반환."""
    sub_sitemaps: list[str] = []
    post_urls: list[str] = []

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        logger.warning("sitemap XML 파싱 실패: %s", exc)
        return sub_sitemaps, post_urls

    tag = root.tag.lower()

    # sitemapindex — 하위 sitemap 목록
    if "sitemapindex" in tag:
        for sitemap in root.findall(f"{{{_SM_NS}}}sitemap"):
            loc = sitemap.findtext(f"{{{_SM_NS}}}loc") or ""
            if loc:
                sub_sitemaps.append(urljoin(root_url, loc.strip()))
        # 네임스페이스 없는 경우도 처리
        for sitemap in root.findall("sitemap"):
            loc = sitemap.findtext("loc") or ""
            if loc:
                sub_sitemaps.append(urljoin(root_url, loc.strip()))
        return sub_sitemaps, post_urls

    # urlset — URL 목록
    for url_elem in root.findall(f"{{{_SM_NS}}}url"):
        loc = url_elem.findtext(f"{{{_SM_NS}}}loc") or ""
        if loc and _looks_like_post(loc.strip()):
            post_urls.append(loc.strip())
    # 네임스페이스 없는 경우
    for url_elem in root.findall("url"):
        loc = url_elem.findtext("loc") or ""
        if loc and _looks_like_post(loc.strip()):
            post_urls.append(loc.strip())

    return sub_sitemaps, post_urls


def _fetch_sitemap_urls(sitemap_url: str, root_url: str, depth: int = 0) -> list[str]:
    """sitemap URL에서 재귀적으로 포스트 URL을 수집한다."""
    if depth > 3:
        return []
    if len(sitemap_url) == 0:
        return []

    try:
        xml_text = fetch_text(sitemap_url)
    except Exception as exc:
        logger.debug("sitemap fetch 실패: %s — %s", sitemap_url, exc)
        return []

    sub_sitemaps, post_urls = _parse_sitemap_xml(xml_text, root_url)

    all_urls = list(post_urls)
    for sub_url in sub_sitemaps:
        if len(all_urls) >= _MAX_URLS:
            break
        sub_posts = _fetch_sitemap_urls(sub_url, root_url, depth + 1)
        all_urls.extend(sub_posts)

    return all_urls[:_MAX_URLS]


def _find_sitemap_url(root_url: str) -> list[str]:
    """root_url에서 sitemap URL을 탐색한다."""
    candidates = [
        urljoin(root_url, "/sitemap.xml"),
        urljoin(root_url, "/sitemap_index.xml"),
        urljoin(root_url, "/sitemap/"),
    ]

    # robots.txt에서 Sitemap: 디렉티브 탐색
    try:
        robots_text = fetch_text(urljoin(root_url, "/robots.txt"))
        for line in robots_text.splitlines():
            if line.lower().startswith("sitemap:"):
                sm_url = line.split(":", 1)[1].strip()
                if sm_url:
                    candidates.insert(0, sm_url)
    except Exception:
        pass

    found: list[str] = []
    for candidate in candidates:
        try:
            xml_text = fetch_text(candidate)
            if "<urlset" in xml_text or "<sitemapindex" in xml_text:
                found.append(candidate)
        except Exception:
            continue

    return found


class SitemapAdapter(BaseAdapter):
    """sitemap.xml 기반 블로그 adapter."""

    name = "sitemap"

    def discover_posts(self, root_url: str) -> list[PostRef]:
        """sitemap에서 글 목록을 반환."""
        sitemap_urls = _find_sitemap_url(root_url)
        if not sitemap_urls:
            logger.info("sitemap을 찾을 수 없음: %s", root_url)
            return []

        all_post_urls: list[str] = []
        for sm_url in sitemap_urls:
            urls = _fetch_sitemap_urls(sm_url, root_url)
            all_post_urls.extend(urls)

        # 중복 제거
        seen: set[str] = set()
        posts: list[PostRef] = []
        for url in all_post_urls:
            if url not in seen:
                seen.add(url)
                posts.append(PostRef(url=url, canonical_url=url))

        logger.info("sitemap discover: %d개 포스트 발견 (%s)", len(posts), root_url)
        return posts[:_MAX_URLS]

    def fetch_post(self, post_ref: PostRef) -> Post:
        """개별 글을 가져온다."""
        url = post_ref.url
        if not can_fetch(url):
            raise PermissionError(f"robots.txt skip: {url}")

        try:
            html_text = fetch_text(url)
        except Exception as exc:
            raise RuntimeError(f"포스트 fetch 실패: {url}") from exc

        from sources.blog.adapters.generic_html import _MetaExtractor, extract_main_content
        meta = _MetaExtractor()
        try:
            meta.feed(html_text)
        except Exception:
            pass

        title = post_ref.title or meta.title or ""
        author = meta.author or None
        published_at = post_ref.published_at or (meta.published_at or None)

        content_html = extract_main_content(html_text)
        markdown = html_to_markdown(content_html)

        canonical = post_ref.canonical_url or url
        post = Post(
            url=url,
            canonical_url=canonical,
            title=title,
            published_at=published_at,
            author=author,
            content_markdown=markdown,
            extras={"adapter": self.name},
        )
        post.lang = self.detect_language(post)
        return post
