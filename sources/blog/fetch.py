"""HTTP 클라이언트 공통 유틸.

User-Agent 설정, rate limiting, robots.txt 확인, 재시도 등을 제공한다.
"""
from __future__ import annotations

import gzip
import logging
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from io import BytesIO

logger = logging.getLogger(__name__)

# ThreadCollector 식별 User-Agent
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 "
    "ThreadCollector/0.1 (blog adapter; personal research)"
)

# robots.txt 캐시: {origin: RobotFileParser}
_robots_cache: dict[str, urllib.robotparser.RobotFileParser] = {}


def _get_robots(root_url: str) -> urllib.robotparser.RobotFileParser | None:
    """root_url에 대한 robots.txt 파서를 캐싱하여 반환."""
    parsed = urllib.parse.urlparse(root_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    if origin in _robots_cache:
        return _robots_cache[origin]

    rp = urllib.robotparser.RobotFileParser()
    robots_url = f"{origin}/robots.txt"
    try:
        rp.set_url(robots_url)
        rp.read()
        _robots_cache[origin] = rp
        return rp
    except Exception as exc:
        # robots.txt 읽기 실패 시 fail-open (수집 진행)
        logger.debug("robots.txt 읽기 실패 (%s): %s — fail-open", robots_url, exc)
        _robots_cache[origin] = None  # type: ignore[assignment]
        return None


def can_fetch(url: str) -> bool:
    """robots.txt 기준으로 해당 URL을 수집해도 되는지 확인."""
    parsed = urllib.parse.urlparse(url)
    root_url = f"{parsed.scheme}://{parsed.netloc}"
    rp = _get_robots(root_url)
    if rp is None:
        return True  # fail-open
    return rp.can_fetch("*", url)


def _build_request(url: str) -> urllib.request.Request:
    """공통 헤더가 포함된 Request 객체를 생성."""
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        },
    )


def fetch_bytes(url: str, timeout: int = 15, retries: int = 2) -> bytes:
    """URL에서 바이트를 가져온다. 재시도(지수 백오프) 포함."""
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        if attempt > 0:
            sleep_sec = 2 ** attempt
            logger.debug("재시도 %d/%d — %s초 후 재요청: %s", attempt, retries, sleep_sec, url)
            time.sleep(sleep_sec)
        try:
            req = _build_request(url)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                # gzip 자동 압축 해제
                encoding = resp.headers.get("Content-Encoding", "")
                if encoding == "gzip":
                    raw = gzip.decompress(raw)
                elif encoding == "deflate":
                    import zlib
                    raw = zlib.decompress(raw)
                return raw
        except Exception as exc:
            last_exc = exc
            logger.debug("fetch 실패 (시도 %d): %s — %s", attempt + 1, url, exc)

    raise RuntimeError(f"fetch 최종 실패: {url}") from last_exc


def fetch_text(url: str, timeout: int = 15, retries: int = 2, encoding: str | None = None) -> str:
    """URL에서 텍스트를 가져온다."""
    raw = fetch_bytes(url, timeout=timeout, retries=retries)
    if encoding:
        return raw.decode(encoding, errors="replace")
    # Content-Type charset 자동 감지 → fallback utf-8
    for enc in ("utf-8", "euc-kr", "cp949", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")
