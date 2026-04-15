"""RSS/Atom 피드 파서 adapter.

feedparser 패키지가 없으면 표준 라이브러리 xml.etree.ElementTree로 직접 파싱.
"""
from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

from sources.blog.adapters.base import BaseAdapter
from sources.blog.collect import Post, PostRef
from sources.blog.fetch import can_fetch, fetch_text
from sources.blog.html_to_md import html_to_markdown

logger = logging.getLogger(__name__)

# Atom/RSS XML 네임스페이스
_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "media": "http://search.yahoo.com/mrss/",
}


# ─────────────────────────────────────────────────────────
# HTML 링크 추출 (피드 URL 탐색용)
# ─────────────────────────────────────────────────────────

class _LinkParser(HTMLParser):
    """<link> 태그에서 RSS/Atom 피드 URL을 추출."""

    def __init__(self) -> None:
        super().__init__()
        self.feed_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "link":
            return
        attr_dict = dict(attrs)
        rel = attr_dict.get("rel", "")
        type_ = attr_dict.get("type", "")
        href = attr_dict.get("href", "")
        if rel == "alternate" and "rss" in type_ or "atom" in type_:
            if href:
                self.feed_urls.append(href)


def _find_feed_url(root_url: str, html_text: str) -> str | None:
    """HTML에서 RSS/Atom 피드 URL을 찾는다."""
    parser = _LinkParser()
    try:
        parser.feed(html_text)
    except Exception:
        pass
    if parser.feed_urls:
        return urljoin(root_url, parser.feed_urls[0])
    return None


def _guess_feed_candidates(root_url: str) -> list[str]:
    """일반적인 피드 URL 후보를 생성."""
    base = root_url.rstrip("/")
    return [
        f"{base}/rss",
        f"{base}/rss.xml",
        f"{base}/feed",
        f"{base}/feed.xml",
        f"{base}/atom.xml",
        f"{base}/feed/",
        f"{base}/rss/",
    ]


# ─────────────────────────────────────────────────────────
# RSS/Atom 파싱
# ─────────────────────────────────────────────────────────

def _parse_date(date_str: str | None) -> str | None:
    """RFC 2822 또는 ISO 8601 날짜 문자열을 YYYY-MM-DD로 변환."""
    if not date_str:
        return None
    date_str = date_str.strip()
    # ISO 8601 형식
    m = re.match(r"(\d{4}-\d{2}-\d{2})", date_str)
    if m:
        return m.group(1)
    # RFC 2822 (RSS pubDate)
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    return None


def _text(elem: ET.Element | None) -> str:
    """XML 요소의 텍스트를 안전하게 가져온다."""
    if elem is None:
        return ""
    return (elem.text or "").strip()


def _find(elem: ET.Element, *paths: str) -> ET.Element | None:
    """여러 XPath 후보 중 처음 찾은 요소를 반환."""
    for path in paths:
        found = elem.find(path, _NS)
        if found is not None:
            return found
    return None


def _parse_rss_feed(xml_text: str, root_url: str) -> list[PostRef]:
    """RSS 2.0 또는 Atom 피드를 파싱해 PostRef 리스트를 반환."""
    posts: list[PostRef] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        logger.warning("XML 파싱 실패: %s", exc)
        return posts

    tag = root.tag.lower()

    # Atom 피드
    if "atom" in tag or root.tag == "{http://www.w3.org/2005/Atom}feed":
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            link_elem = entry.find("{http://www.w3.org/2005/Atom}link[@rel='alternate']")
            if link_elem is None:
                link_elem = entry.find("{http://www.w3.org/2005/Atom}link")
            url = link_elem.get("href", "") if link_elem is not None else ""
            if not url:
                continue
            url = urljoin(root_url, url)

            title_elem = entry.find("{http://www.w3.org/2005/Atom}title")
            title = _text(title_elem)

            pub_elem = _find(
                entry,
                "{http://www.w3.org/2005/Atom}published",
                "{http://www.w3.org/2005/Atom}updated",
            )
            pub_date = _parse_date(_text(pub_elem))

            posts.append(PostRef(url=url, title=title or None, published_at=pub_date, canonical_url=url))
        return posts

    # RSS 2.0
    channel = root.find("channel")
    if channel is None:
        channel = root  # 일부 피드는 channel 없이 바로 item
    for item in channel.findall("item"):
        link_elem = item.find("link")
        url = _text(link_elem)
        if not url:
            guid = item.find("guid")
            url = _text(guid)
        if not url:
            continue
        url = urljoin(root_url, url)

        title_elem = item.find("title")
        title = _text(title_elem)

        pub_date = _parse_date(_text(item.find("pubDate")))

        posts.append(PostRef(url=url, title=title or None, published_at=pub_date, canonical_url=url))

    return posts


def _extract_content_from_feed_item(xml_text: str, url: str) -> str | None:
    """피드 XML에서 특정 URL 항목의 content를 추출."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None

    # RSS 2.0 items
    channel = root.find("channel") or root
    for item in channel.findall("item"):
        link_elem = item.find("link")
        item_url = _text(link_elem)
        if item_url != url:
            continue
        # content:encoded 우선
        content_elem = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")
        if content_elem is not None and content_elem.text:
            return content_elem.text
        # description fallback
        desc_elem = item.find("description")
        if desc_elem is not None and desc_elem.text:
            return desc_elem.text

    # Atom entries
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        link_elem = entry.find("{http://www.w3.org/2005/Atom}link")
        entry_url = link_elem.get("href", "") if link_elem is not None else ""
        if entry_url != url:
            continue
        content_elem = entry.find("{http://www.w3.org/2005/Atom}content")
        if content_elem is not None and content_elem.text:
            return content_elem.text
        summary_elem = entry.find("{http://www.w3.org/2005/Atom}summary")
        if summary_elem is not None and summary_elem.text:
            return summary_elem.text

    return None


# ─────────────────────────────────────────────────────────
# RssAdapter
# ─────────────────────────────────────────────────────────

class RssAdapter(BaseAdapter):
    """RSS/Atom 피드 기반 블로그 adapter."""

    name = "rss"

    def __init__(self) -> None:
        self._feed_url_cache: dict[str, str] = {}  # root_url → feed_url
        self._feed_xml_cache: dict[str, str] = {}   # feed_url → xml_text

    def _resolve_feed_url(self, root_url: str) -> str | None:
        """root_url에서 RSS/Atom 피드 URL을 찾는다."""
        if root_url in self._feed_url_cache:
            return self._feed_url_cache[root_url]

        # HTML에서 <link rel="alternate"> 탐색
        try:
            html_text = fetch_text(root_url)
            feed_url = _find_feed_url(root_url, html_text)
            if feed_url:
                self._feed_url_cache[root_url] = feed_url
                return feed_url
        except Exception as exc:
            logger.debug("root_url HTML 읽기 실패: %s — %s", root_url, exc)

        # 후보 URL 시도
        for candidate in _guess_feed_candidates(root_url):
            try:
                xml_text = fetch_text(candidate)
                # RSS/Atom 피드인지 확인
                if "<rss" in xml_text[:500] or "<feed" in xml_text[:500] or "<?xml" in xml_text[:100]:
                    self._feed_url_cache[root_url] = candidate
                    self._feed_xml_cache[candidate] = xml_text
                    return candidate
            except Exception:
                continue

        return None

    def _get_feed_xml(self, feed_url: str) -> str | None:
        """피드 XML을 가져온다 (캐시 활용)."""
        if feed_url in self._feed_xml_cache:
            return self._feed_xml_cache[feed_url]
        try:
            xml_text = fetch_text(feed_url)
            self._feed_xml_cache[feed_url] = xml_text
            return xml_text
        except Exception as exc:
            logger.warning("피드 XML 읽기 실패: %s — %s", feed_url, exc)
            return None

    def discover_posts(self, root_url: str) -> list[PostRef]:
        """피드에서 글 목록을 반환."""
        feed_url = self._resolve_feed_url(root_url)
        if not feed_url:
            logger.info("RSS/Atom 피드를 찾을 수 없음: %s", root_url)
            return []

        xml_text = self._get_feed_xml(feed_url)
        if not xml_text:
            return []

        posts = _parse_rss_feed(xml_text, root_url)
        logger.info("RSS discover: %d개 포스트 발견 (%s)", len(posts), feed_url)
        return posts

    def fetch_post(self, post_ref: PostRef) -> Post:
        """개별 글을 가져온다."""
        url = post_ref.url

        # 먼저 피드 XML에서 content 추출 시도 (robots.txt 확인 전 — 피드에서 이미 허용된 콘텐츠)
        feed_xml: str | None = None
        for cached_xml in self._feed_xml_cache.values():
            content_html = _extract_content_from_feed_item(cached_xml, url)
            if content_html:
                feed_xml = content_html
                break

        if feed_xml and len(feed_xml) > 200:
            markdown = html_to_markdown(feed_xml)
        else:
            # 직접 HTTP fetch — robots.txt 확인
            if not can_fetch(url):
                raise PermissionError(f"robots.txt에 의해 skip: {url}")
            try:
                html_text = fetch_text(url)
            except Exception as exc:
                raise RuntimeError(f"포스트 fetch 실패: {url}") from exc

            # 본문 추출 (generic 로직)
            from sources.blog.adapters.generic_html import extract_main_content
            content_html = extract_main_content(html_text)
            markdown = html_to_markdown(content_html)

        title = post_ref.title or ""
        published_at = post_ref.published_at
        canonical = post_ref.canonical_url or url

        post = Post(
            url=url,
            canonical_url=canonical,
            title=title,
            published_at=published_at,
            author=None,
            content_markdown=markdown,
            extras={"adapter": self.name},
        )
        post.lang = self.detect_language(post)
        return post
