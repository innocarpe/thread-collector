"""Generic HTML 블로그 크롤러 (최종 fallback adapter).

RSS/sitemap이 없는 블로그에서 링크를 수집하고 본문을 추출한다.
"""
from __future__ import annotations

import logging
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

from sources.blog.adapters.base import BaseAdapter
from sources.blog.collect import Post, PostRef
from sources.blog.fetch import can_fetch, fetch_text
from sources.blog.html_to_md import html_to_markdown

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# HTML 파서 유틸
# ─────────────────────────────────────────────────────────

class _LinkExtractor(HTMLParser):
    """<a href> 링크를 수집하는 파서."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            attr_dict = dict(attrs)
            href = attr_dict.get("href", "") or ""
            if href and not href.startswith(("#", "javascript:", "mailto:")):
                self.links.append(href)


class _MetaExtractor(HTMLParser):
    """<meta>, <title>, <time> 태그에서 메타데이터를 추출."""

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.author = ""
        self.published_at = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_dict = dict(attrs)

        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (attr_dict.get("name") or attr_dict.get("property") or "").lower()
            content = attr_dict.get("content", "") or ""
            if name in ("og:title", "twitter:title") and not self.title:
                self.title = content
            elif name == "author":
                self.author = content
            elif name in ("article:published_time", "datePublished"):
                self.published_at = content[:10]
        elif tag == "time":
            dt = attr_dict.get("datetime", "") or ""
            if dt and not self.published_at:
                self.published_at = dt[:10]

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title and not self.title:
            self.title = data.strip()


class _ContentBlockFinder(HTMLParser):
    """가장 많은 <p> 태그를 포함하는 블록(article/main/div)을 찾는다."""

    def __init__(self) -> None:
        super().__init__()
        self._stack: list[dict] = []   # {tag, depth, content, p_count}
        self._depth = 0
        self.best_html = ""
        self._best_p_count = 0
        self._skip_depth = 0

    _SKIP_TAGS = {"script", "style", "nav", "footer", "header", "aside"}
    _BLOCK_TAGS = {"article", "main", "section", "div"}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self._SKIP_TAGS:
            self._skip_depth += 1
        if self._skip_depth > 0:
            return
        self._depth += 1
        if tag in self._BLOCK_TAGS:
            self._stack.append({"tag": tag, "depth": self._depth, "html": f"<{tag}>", "p_count": 0})
        elif tag == "p" and self._stack:
            self._stack[-1]["p_count"] += 1
            # 상위 스택에도 p_count 전파
            for item in self._stack[:-1]:
                item["p_count"] += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self._SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        if self._skip_depth > 0:
            return
        self._depth -= 1
        if tag in self._BLOCK_TAGS and self._stack:
            block = self._stack.pop()
            if block["p_count"] > self._best_p_count:
                self._best_p_count = block["p_count"]
                self.best_html = block.get("html", "")

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        if self._stack:
            self._stack[-1]["html"] = self._stack[-1].get("html", "") + data


def _extract_block_with_regex(html_text: str, selector: str) -> str | None:
    """정규식으로 특정 class/id 블록을 추출."""
    # class 또는 id로 태그 찾기
    pattern = re.compile(
        rf'<(?:article|div|section|main)[^>]*(?:class|id)=["\'][^"\']*{re.escape(selector)}[^"\']*["\'][^>]*>',
        re.IGNORECASE | re.DOTALL,
    )
    m = pattern.search(html_text)
    if not m:
        return None

    start = m.start()
    tag_match = re.match(r"<(\w+)", html_text[start:])
    if not tag_match:
        return None
    tag = tag_match.group(1).lower()

    # 중첩 태그 추적으로 끝 위치 찾기
    pos = start + len(m.group(0))
    depth = 1
    open_pat = re.compile(rf"<{tag}[\s>]", re.IGNORECASE)
    close_pat = re.compile(rf"</{tag}>", re.IGNORECASE)

    while depth > 0 and pos < len(html_text):
        next_open = open_pat.search(html_text, pos)
        next_close = close_pat.search(html_text, pos)

        if next_close is None:
            break
        if next_open is not None and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            pos = next_close.end()

    return html_text[start:pos]


def extract_main_content(html_text: str, selectors: list[str] | None = None) -> str:
    """HTML에서 본문 블록을 추출한다.

    selectors: class/id 이름 후보 (없으면 자동 탐지)
    """
    # 1. 주어진 selector 시도
    if selectors:
        for sel in selectors:
            block = _extract_block_with_regex(html_text, sel)
            if block and block.count("<p") >= 2:
                return block

    # 2. <article> 태그 우선
    article_m = re.search(r"<article[^>]*>(.*?)</article>", html_text, re.IGNORECASE | re.DOTALL)
    if article_m:
        inner = article_m.group(0)
        if inner.count("<p") >= 2:
            return inner

    # 3. <main> 태그
    main_m = re.search(r"<main[^>]*>(.*?)</main>", html_text, re.IGNORECASE | re.DOTALL)
    if main_m:
        inner = main_m.group(0)
        if inner.count("<p") >= 2:
            return inner

    # 4. 가장 많은 <p>를 포함한 div 블록
    common_selectors = [
        "entry-content", "post-content", "article-content",
        "content", "post-body", "blog-post", "entry",
    ]
    for sel in common_selectors:
        block = _extract_block_with_regex(html_text, sel)
        if block and block.count("<p") >= 2:
            return block

    # 5. 전체 body fallback
    body_m = re.search(r"<body[^>]*>(.*?)</body>", html_text, re.IGNORECASE | re.DOTALL)
    if body_m:
        return body_m.group(0)

    return html_text


def _is_post_url(url: str, root_domain: str) -> bool:
    """URL이 블로그 포스트처럼 보이는지 확인."""
    parsed = urlparse(url)
    # 같은 도메인만
    if parsed.netloc and parsed.netloc != root_domain:
        return False
    path = parsed.path

    # 쿼리스트링 있으면 제외
    if parsed.query:
        return False

    # 블로그스러운 URL 패턴
    post_patterns = [
        r"/\d{4}/\d{2}/",       # /2024/06/
        r"/post/",
        r"/posts/",
        r"/blog/",
        r"/entry/",
        r"/\d+$",               # Tistory 스타일: /123
        r"/\d+/",
        r"[a-z0-9-]{10,}$",     # 긴 slug
    ]
    for pattern in post_patterns:
        if re.search(pattern, path, re.IGNORECASE):
            return True

    return False


# ─────────────────────────────────────────────────────────
# GenericHtmlAdapter
# ─────────────────────────────────────────────────────────

class GenericHtmlAdapter(BaseAdapter):
    """RSS/sitemap이 없는 블로그용 fallback HTML 크롤러."""

    name = "generic_html"

    def discover_posts(self, root_url: str) -> list[PostRef]:
        """root URL에서 링크를 수집하고 포스트 URL 후보를 반환."""
        if not can_fetch(root_url):
            logger.warning("robots.txt skip: %s", root_url)
            return []

        try:
            html_text = fetch_text(root_url)
        except Exception as exc:
            logger.error("root URL fetch 실패: %s — %s", root_url, exc)
            return []

        parsed_root = urlparse(root_url)
        root_domain = parsed_root.netloc

        extractor = _LinkExtractor()
        try:
            extractor.feed(html_text)
        except Exception:
            pass

        seen: set[str] = set()
        posts: list[PostRef] = []
        for raw_href in extractor.links:
            url = urljoin(root_url, raw_href).split("#")[0].rstrip("/")
            if url in seen:
                continue
            seen.add(url)
            if _is_post_url(url, root_domain):
                posts.append(PostRef(url=url, canonical_url=url))

        logger.info("generic_html discover: %d개 포스트 후보 (%s)", len(posts), root_url)
        return posts

    def fetch_post(self, post_ref: PostRef) -> Post:
        """개별 글을 가져온다."""
        url = post_ref.url
        if not can_fetch(url):
            raise PermissionError(f"robots.txt skip: {url}")

        try:
            html_text = fetch_text(url)
        except Exception as exc:
            raise RuntimeError(f"포스트 fetch 실패: {url}") from exc

        # 메타데이터 추출
        meta = _MetaExtractor()
        try:
            meta.feed(html_text)
        except Exception:
            pass

        title = post_ref.title or meta.title or ""
        author = meta.author or None
        published_at = post_ref.published_at or (meta.published_at or None)

        # 본문 추출
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
            raw_html=content_html,
            extras={"adapter": self.name},
        )
        post.lang = self.detect_language(post)
        return post
