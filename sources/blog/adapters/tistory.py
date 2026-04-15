"""Tistory 전용 adapter.

Tistory 블로그는 {blog}/rss 피드를 제공하며 sitemap.xml도 지원한다.
본문 추출은 스킨마다 다른 CSS selector를 여러 개 시도한다.

최우선 타겟: soulduse.tistory.com
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

# Tistory 본문 CSS selector 후보 (스킨별 다름, 우선순위 순)
_CONTENT_SELECTORS = [
    "tt_article_useless_p_margin",   # 구 스킨
    "contents_style",                # 새 스킨
    "entry-content",
    "article_view",
    "post-content",
    "article-content",
    "entry",
    "content",
]

# 제목 selector 후보
_TITLE_SELECTORS = [
    "title_view",
    "tit_post",
    "post-title",
    "article-title",
    "entry-title",
]

# 날짜 selector 후보
_DATE_SELECTORS = [
    "txt_date",
    "date",
    "post-date",
    "article-date",
]


# ─────────────────────────────────────────────────────────
# HTML 파서 유틸
# ─────────────────────────────────────────────────────────

class _TistoryMetaParser(HTMLParser):
    """Tistory HTML에서 제목·날짜·저자를 추출."""

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.author = ""
        self.published_at = ""
        self._in_title_tag = False
        self._in_target = False
        self._target_class = ""
        self._target_depth = 0
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_lower = tag.lower()
        attr_dict = dict(attrs)
        cls = attr_dict.get("class", "") or ""
        id_ = attr_dict.get("id", "") or ""

        # <title> 태그
        if tag_lower == "title":
            self._in_title_tag = True

        # meta 태그
        if tag_lower == "meta":
            name = (attr_dict.get("name") or attr_dict.get("property") or "").lower()
            content = attr_dict.get("content", "") or ""
            if name in ("og:title",) and not self.title:
                self.title = content
            elif name == "author" and not self.author:
                self.author = content
            elif name in ("article:published_time", "datepublished") and not self.published_at:
                self.published_at = content[:10]

        # <time datetime="">
        if tag_lower == "time":
            dt = attr_dict.get("datetime", "") or ""
            if dt and not self.published_at:
                self.published_at = dt[:10]

        # 특정 class의 span/div 탐색
        combined = f"{cls} {id_}".lower()
        for sel in _DATE_SELECTORS:
            if sel in combined:
                self._in_target = True
                self._target_class = sel
                self._target_depth = 1
                self._buf = []
                break

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title_tag = False
        if self._in_target:
            self._target_depth -= 1
            if self._target_depth <= 0:
                text = "".join(self._buf).strip()
                if text and not self.published_at:
                    # 날짜 형식 파싱
                    m = re.search(r"(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})", text)
                    if m:
                        self.published_at = f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"
                self._in_target = False

    def handle_data(self, data: str) -> None:
        if self._in_title_tag and not self.title:
            self.title = data.strip()
        if self._in_target:
            self._buf.append(data)


def _extract_tistory_content(html_text: str) -> str:
    """Tistory HTML에서 본문 블록을 추출한다."""
    from sources.blog.adapters.generic_html import _extract_block_with_regex

    for sel in _CONTENT_SELECTORS:
        block = _extract_block_with_regex(html_text, sel)
        if block and block.count("<p") >= 1:
            # 광고 제거
            block = re.sub(r'<div[^>]*class="[^"]*ad[^"]*"[^>]*>.*?</div>', "", block, flags=re.IGNORECASE | re.DOTALL)
            return block

    # fallback: <article>
    m = re.search(r"<article[^>]*>(.*?)</article>", html_text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(0)

    # fallback: <main>
    m = re.search(r"<main[^>]*>(.*?)</main>", html_text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(0)

    return html_text


# ─────────────────────────────────────────────────────────
# RSS 파싱 (Tistory 전용)
# ─────────────────────────────────────────────────────────

def _parse_tistory_rss(xml_text: str, root_url: str) -> list[PostRef]:
    """Tistory RSS 피드를 파싱해 PostRef 리스트를 반환."""
    posts: list[PostRef] = []

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        logger.warning("Tistory RSS XML 파싱 실패: %s", exc)
        return posts

    channel = root.find("channel")
    if channel is None:
        channel = root

    for item in channel.findall("item"):
        link_elem = item.find("link")
        url = (link_elem.text or "").strip() if link_elem is not None else ""

        # Tistory RSS의 link 태그는 종종 CDATA로 감싸거나 next sibling text
        if not url:
            # link 뒤의 text node
            for child in item:
                if child.tag == "link":
                    url = (child.text or "").strip()
                    if not url and child.tail:
                        url = child.tail.strip()
                    break

        if not url:
            guid = item.find("guid")
            url = (guid.text or "").strip() if guid is not None else ""

        if not url:
            continue
        url = urljoin(root_url, url)

        title_elem = item.find("title")
        title = (title_elem.text or "").strip() if title_elem is not None else ""
        # CDATA 제거
        title = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", title, flags=re.DOTALL).strip()

        pub_date_elem = item.find("pubDate")
        pub_str = (pub_date_elem.text or "").strip() if pub_date_elem is not None else ""
        pub_date: str | None = None
        if pub_str:
            try:
                dt = parsedate_to_datetime(pub_str)
                pub_date = dt.strftime("%Y-%m-%d")
            except Exception:
                m = re.search(r"(\d{4}-\d{2}-\d{2})", pub_str)
                if m:
                    pub_date = m.group(1)

        posts.append(PostRef(url=url, title=title or None, published_at=pub_date, canonical_url=url))

    return posts


# ─────────────────────────────────────────────────────────
# TistoryAdapter
# ─────────────────────────────────────────────────────────

class TistoryAdapter(BaseAdapter):
    """Tistory 블로그 전용 adapter.

    접근 순서:
    1. {root}/rss 피드 파싱
    2. {root}/sitemap.xml 병합 (rss가 부족할 때)
    3. fetch_post: HTML 본문 selector로 추출
    """

    name = "tistory"

    def __init__(self) -> None:
        self._rss_cache: dict[str, str] = {}  # root_url → xml_text

    def _get_rss(self, root_url: str) -> str | None:
        """Tistory RSS 피드를 가져온다."""
        if root_url in self._rss_cache:
            return self._rss_cache[root_url]

        base = root_url.rstrip("/")
        rss_url = f"{base}/rss"
        try:
            xml_text = fetch_text(rss_url)
            if "<rss" in xml_text[:500] or "<?xml" in xml_text[:100]:
                self._rss_cache[root_url] = xml_text
                logger.debug("Tistory RSS 로드 성공: %s", rss_url)
                return xml_text
        except Exception as exc:
            logger.debug("Tistory RSS 로드 실패: %s — %s", rss_url, exc)

        return None

    def _get_sitemap_posts(self, root_url: str) -> list[PostRef]:
        """Tistory sitemap에서 포스트 URL을 가져온다."""
        from sources.blog.adapters.sitemap import _fetch_sitemap_urls

        base = root_url.rstrip("/")
        sitemap_url = f"{base}/sitemap.xml"
        try:
            urls = _fetch_sitemap_urls(sitemap_url, root_url)
            return [PostRef(url=u, canonical_url=u) for u in urls]
        except Exception as exc:
            logger.debug("Tistory sitemap 실패: %s — %s", sitemap_url, exc)
            return []

    def discover_posts(self, root_url: str) -> list[PostRef]:
        """Tistory 블로그 글 목록을 반환.

        RSS 먼저 시도, 부족하면 sitemap 병합.
        """
        posts: list[PostRef] = []
        seen_urls: set[str] = set()

        # 1. RSS 파싱
        rss_xml = self._get_rss(root_url)
        if rss_xml:
            rss_posts = _parse_tistory_rss(rss_xml, root_url)
            for p in rss_posts:
                if p.url not in seen_urls:
                    seen_urls.add(p.url)
                    posts.append(p)
            logger.info("Tistory RSS: %d개 포스트", len(rss_posts))

        # 2. sitemap 병합 (항상 — RSS는 최근 20개만 반환하므로 전량 수집을 위해 병합)
        if True:
            sitemap_posts = self._get_sitemap_posts(root_url)
            merged = 0
            for p in sitemap_posts:
                if p.url not in seen_urls:
                    seen_urls.add(p.url)
                    posts.append(p)
                    merged += 1
            if merged:
                logger.info("Tistory sitemap 병합: %d개 추가", merged)

        logger.info("Tistory discover 완료: 총 %d개 포스트 (%s)", len(posts), root_url)
        return posts

    def fetch_post(self, post_ref: PostRef) -> Post:
        """Tistory 개별 글을 가져온다."""
        url = post_ref.url
        if not can_fetch(url):
            raise PermissionError(f"robots.txt skip: {url}")

        try:
            html_text = fetch_text(url)
        except Exception as exc:
            raise RuntimeError(f"포스트 fetch 실패: {url}") from exc

        # 메타데이터 추출
        meta = _TistoryMetaParser()
        try:
            meta.feed(html_text)
        except Exception:
            pass

        title = post_ref.title or meta.title or ""
        author = meta.author or None
        published_at = post_ref.published_at or (meta.published_at or None)

        # 본문 추출
        content_html = _extract_tistory_content(html_text)
        markdown = html_to_markdown(content_html)

        canonical = post_ref.canonical_url or url
        post = Post(
            url=url,
            canonical_url=canonical,
            title=title,
            published_at=published_at,
            author=author,
            content_markdown=markdown,
            raw_html=content_html,
            extras={"adapter": self.name},
        )
        post.lang = self.detect_language(post)
        return post
