"""HTML → Markdown 변환 유틸.

html2text 패키지가 있으면 사용하고, 없으면 표준 라이브러리 html.parser 기반
간이 변환기를 사용한다.
"""
from __future__ import annotations

import html
import re
from html.parser import HTMLParser


def _try_html2text(html_str: str) -> str | None:
    """html2text 패키지로 변환. 설치 안 됐으면 None 반환."""
    try:
        import html2text as h2t  # type: ignore[import]
        converter = h2t.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = True
        converter.body_width = 0  # 줄 바꿈 없음
        return converter.handle(html_str)
    except ImportError:
        return None


# --- 간이 HTML→Markdown 변환기 (표준 라이브러리 기반) ---

# 무시할 태그
_SKIP_TAGS = {
    "script", "style", "head", "meta", "link", "noscript",
    "iframe", "svg", "nav", "header", "footer", "aside",
}

# 인라인 태그
_INLINE_TAGS = {"a", "span", "strong", "b", "em", "i", "code", "mark", "time", "abbr"}


class _SimpleMarkdownParser(HTMLParser):
    """HTML을 간이 Markdown으로 변환하는 파서."""

    def __init__(self) -> None:
        super().__init__()
        self._buf: list[str] = []
        self._skip_depth = 0          # 무시 태그 안에 있는 깊이
        self._list_stack: list[str] = []  # 'ul' or 'ol'
        self._ol_counter: list[int] = []
        self._heading_level = 0
        self._in_pre = False
        self._in_code = False
        self._in_a = False
        self._a_href = ""
        self._a_text: list[str] = []

    # --- 내부 헬퍼 ---

    def _emit(self, text: str) -> None:
        if self._skip_depth == 0:
            self._buf.append(text)

    def _heading_prefix(self, level: int) -> str:
        return "#" * min(level, 6) + " "

    def _current_list_indent(self) -> str:
        return "  " * (len(self._list_stack) - 1)

    # --- HTMLParser 오버라이드 ---

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth > 0:
            return

        attr_dict = dict(attrs)

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self._heading_level = level
            self._emit("\n\n" + self._heading_prefix(level))
        elif tag == "p":
            self._emit("\n\n")
        elif tag == "br":
            self._emit("  \n")
        elif tag in ("ul", "ol"):
            self._list_stack.append(tag)
            self._ol_counter.append(0)
            self._emit("\n")
        elif tag == "li":
            indent = self._current_list_indent()
            list_type = self._list_stack[-1] if self._list_stack else "ul"
            if list_type == "ol":
                self._ol_counter[-1] += 1
                self._emit(f"\n{indent}{self._ol_counter[-1]}. ")
            else:
                self._emit(f"\n{indent}- ")
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("_")
        elif tag == "code":
            self._in_code = True
            if self._in_pre:
                pass  # pre > code는 펜스드 코드블록으로 처리
            else:
                self._emit("`")
        elif tag == "pre":
            self._in_pre = True
            self._emit("\n\n```\n")
        elif tag == "a":
            self._in_a = True
            self._a_href = attr_dict.get("href", "") or ""
            self._a_text = []
        elif tag == "blockquote":
            self._emit("\n\n> ")
        elif tag == "hr":
            self._emit("\n\n---\n\n")
        elif tag == "img":
            alt = attr_dict.get("alt", "") or ""
            src = attr_dict.get("src", "") or ""
            # 이미지는 alt text만 보존
            if alt:
                self._emit(f"[이미지: {alt}]")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in _SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth > 0:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading_level = 0
            self._emit("\n\n")
        elif tag == "p":
            self._emit("\n")
        elif tag in ("ul", "ol"):
            if self._list_stack:
                self._list_stack.pop()
            if self._ol_counter:
                self._ol_counter.pop()
            self._emit("\n")
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("_")
        elif tag == "code":
            self._in_code = False
            if not self._in_pre:
                self._emit("`")
        elif tag == "pre":
            self._in_pre = False
            self._in_code = False
            self._emit("\n```\n\n")
        elif tag == "a":
            text = "".join(self._a_text).strip()
            href = self._a_href
            self._in_a = False
            if href and text:
                self._emit(f"[{text}]({href})")
            elif text:
                self._emit(text)
            self._a_text = []
            self._a_href = ""

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        if self._in_a:
            self._a_text.append(data)
            return
        # HTML 엔티티 디코딩
        text = html.unescape(data)
        if self._in_pre:
            self._emit(text)
        else:
            # 연속 공백·줄바꿈 정리
            text = re.sub(r"[ \t]+", " ", text)
            self._emit(text)

    def handle_entityref(self, name: str) -> None:
        self.handle_data(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.handle_data(f"&#{name};")

    def get_markdown(self) -> str:
        raw = "".join(self._buf)
        # 3개 이상 연속 빈 줄 → 2개로
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def html_to_markdown(html_str: str) -> str:
    """HTML 문자열을 Markdown으로 변환.

    html2text 패키지가 있으면 사용하고, 없으면 간이 변환기를 사용한다.
    """
    result = _try_html2text(html_str)
    if result is not None:
        return result.strip()

    parser = _SimpleMarkdownParser()
    try:
        parser.feed(html_str)
        return parser.get_markdown()
    except Exception:
        # 변환 실패 시 태그만 제거한 평문 반환
        clean = re.sub(r"<[^>]+>", " ", html_str)
        clean = html.unescape(clean)
        clean = re.sub(r"\s+", " ", clean)
        return clean.strip()
