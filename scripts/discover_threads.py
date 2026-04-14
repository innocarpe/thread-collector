#!/usr/bin/env python3
"""
ThreadCollector — discover candidate Threads.net users to collect next.

Phase 1: Corpus mention mining (기본 동작, 하위호환 유지).
Phase 2: Profile enrichment via SSR JSON blob (--enrich).
Phase 3: Keyword search (--sources search --query "...") + hashtag page (--sources hashtag --hashtag ...).
Phase 4: Explore skeleton (NotImplementedError stub).

Usage (Phase 1 기본):
    python3 scripts/discover_threads.py
    python3 scripts/discover_threads.py --interest ai-llm,monetization
    python3 scripts/discover_threads.py --limit 15 --min-mentions 2

Usage (Phase 2+3):
    python3 scripts/discover_threads.py --enrich
    python3 scripts/discover_threads.py --sources corpus,search --query "AI 수익화" --enrich
    python3 scripts/discover_threads.py --sources corpus,hashtag --hashtag ai_llm
    python3 scripts/discover_threads.py --sources corpus,search,hashtag \\
        --query "바이브코딩" --hashtag ai_llm --enrich
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Callable

THREADS_ROOT = Path("Threads")
OUTPUT_ROOT = Path(".claude/discover-threads")
INTEREST_FILE = Path(".thread-collector-interests.json")

MENTION_RE = re.compile(r"@([a-zA-Z0-9_.]{2,30})")

# Noise handles to never treat as candidates.
NOISE_HANDLES = {
    "threads", "youtube", "instagram", "gmail", "naver", "daum", "x",
    "anthropic", "openai", "google", "x.com", "claude", "chatgpt",
    "github", "notion", "vercel", "apple", "meta", "linkedin",
}

CATEGORY_SLUGS = [
    "ai-llm", "viral-sns", "monetization", "dev-tools",
    "product-strategy", "startup-philosophy", "career-growth",
    "learning-retro", "productivity", "web-app",
]


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass
class Candidate:
    handle: str

    # ── Phase 1 필드 (유지) ───────────────────────────────────────────────────
    mentions: int = 0
    category_counts: Counter = field(default_factory=Counter)
    source_users: set = field(default_factory=set)
    contexts: list = field(default_factory=list)  # list of (src_user, snippet)
    score: float = 0.0

    # ── Phase 2 enrichment ────────────────────────────────────────────────────
    bio: str | None = None
    follower_count: int | None = None
    is_private: bool | None = None
    is_verified: bool | None = None
    full_name: str | None = None
    recent_posts: list = field(default_factory=list)  # list of {text, taken_at}
    enrich_status: str = "skipped"  # "success" | "failed" | "private" | "skipped"

    # ── Phase 3/4 소스 추적 ───────────────────────────────────────────────────
    discovered_via: set = field(default_factory=set)  # {"corpus","search","hashtag","explore"}
    search_queries: list = field(default_factory=list)
    hashtag_matches: list = field(default_factory=list)
    explore_rank: int | None = None


@dataclass
class DiscoverConfig:
    """전체 discover 파이프라인 설정."""
    sources: list  # ["corpus", "search", "hashtag", "explore"]
    interests: list
    existing: set = field(default_factory=set)  # 이미 수집된 handle 제외용
    enrich: bool = False
    queries: list = field(default_factory=list)   # search 소스용 키워드 목록
    hashtags: list = field(default_factory=list)  # hashtag 소스용 태그 목록
    min_mentions: int = 2
    limit: int = 20
    enrich_limit: int = 10
    weights: dict = field(default_factory=lambda: {
        "corpus": 3.0, "search": 1.0, "hashtag": 1.0, "explore": 2.0
    })


# ── browse helpers (copied from collect.py) ───────────────────────────────────
# 의존성 없는 단일 파일 유지를 위해 인라인 복사. 장기적으로는 scripts/browse_utils.py 공통화 권장.

_DT_BROWSE_BIN = os.path.expanduser("~/.claude/skills/gstack/browse/dist/browse")
_DT_BROWSE_SRC = os.path.expanduser("~/.claude/skills/gstack/browse/src/cli.ts")
_DT_BROWSE_CMD: list = []  # resolved at first call


def _dt_resolve_browse_cmd() -> list:
    """browse CLI 실행 커맨드를 결정한다 (바이너리 → bun fallback)."""
    if os.path.isfile(_DT_BROWSE_BIN) and os.access(_DT_BROWSE_BIN, os.X_OK):
        try:
            r = subprocess.run(
                [_DT_BROWSE_BIN, "--help"],
                capture_output=True, timeout=5,
            )
            if r.returncode not in (137, -9):
                return [_DT_BROWSE_BIN]
        except Exception:
            pass

    bun = os.path.expanduser("~/.bun/bin/bun")
    if not os.path.isfile(bun):
        import shutil
        bun = shutil.which("bun") or bun
    if os.path.isfile(bun) and os.path.isfile(_DT_BROWSE_SRC):
        return [bun, "run", _DT_BROWSE_SRC]

    return [_DT_BROWSE_BIN]


def _dt_browse_run(args: list, **kwargs) -> subprocess.CompletedProcess:
    """browse 서브커맨드를 실행한다."""
    global _DT_BROWSE_CMD
    if not _DT_BROWSE_CMD:
        _DT_BROWSE_CMD = _dt_resolve_browse_cmd()
    return subprocess.run(_DT_BROWSE_CMD + args, **kwargs)


def _dt_browse_goto(url: str) -> None:
    """browse 브라우저를 URL 로 이동한다."""
    _dt_browse_run(["goto", url], capture_output=True, timeout=30)


def _dt_browse_eval(js: str, tmp_path: str = "/tmp/_dt_eval.js") -> str:
    """JS 를 임시 파일에 저장한 뒤 browse eval 로 실행하고 stdout+stderr 를 반환한다."""
    with open(tmp_path, "w", encoding="utf-8") as fh:
        fh.write(js)
    result = _dt_browse_run(
        ["eval", tmp_path],
        capture_output=True, text=True, timeout=120,
    )
    return (result.stdout + result.stderr).strip()


def _dt_parse_json(output: str) -> dict | None:
    """browse eval 출력에서 첫 번째 JSON 오브젝트 라인을 파싱한다."""
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                pass
    return None


def _decode_unicode_escapes(s: str | None) -> str | None:
    r"""SSR 블롭에서 추출한 문자열의 \uXXXX 리터럴을 실제 유니코드로 변환한다.

    JS 정규식이 JSON 문자열 안의 \\uXXXX 이스케이프를 그대로 캡처하면
    Python json.loads 이후에도 \\uXXXX 리터럴이 남는다.
    서로게이트 페어(\\uD800-\\uDFFF)는 두 개를 묶어 U+10000 이상 코드포인트로 변환한다.
    """
    if not s or r"\u" not in s:
        return s
    try:
        # 서로게이트 페어 먼저 처리 (\uD800-\uDBFF 뒤에 \uDC00-\uDFFF)
        def _replace_pair(m: re.Match) -> str:
            codes = [int(x, 16) for x in re.findall(r"[0-9a-fA-F]{4}", m.group(0))]
            high, low = codes[0], codes[1]
            return chr(0x10000 + (high - 0xD800) * 0x400 + (low - 0xDC00))

        s = re.sub(
            r"\\u[Dd][89AaBb][0-9a-fA-F]{2}\\u[Dd][C-Fc-f][0-9a-fA-F]{2}",
            _replace_pair, s,
        )
        # 나머지 \uXXXX 처리
        s = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), s)
        return s
    except Exception:
        return s


# ── JavaScript templates (discover 전용) ──────────────────────────────────────

# SSR 블롭에서 userID 추출 (collect.py JS_GET_USERID 인라인 복사)
# USERNAME_PLACEHOLDER → handle (@ 제외)
JS_GET_USERID_DT = r"""
(function(targetUsername) {
  const scripts = Array.from(document.querySelectorAll("script"));
  let userId = null;

  // Pass 1: find pk in the same script block as the target username
  for (const s of scripts) {
    const t = s.textContent;
    const idx = t.indexOf('"' + targetUsername + '"');
    if (idx >= 0) {
      const snippet = t.slice(Math.max(0, idx - 300), idx + 300);
      const m = snippet.match(/"pk"\s*:\s*"(\d{10,})"/);
      if (m) { userId = m[1]; break; }
      const m2 = snippet.match(/"user_id"\s*:\s*"(\d{10,})"/);
      if (m2) { userId = m2[1]; break; }
    }
  }

  // Pass 2: fallback — first "userID" in any script
  if (!userId) {
    for (const s of scripts) {
      const t = s.textContent;
      const m = t.match(/"userID"\s*:\s*"(\d{10,})"/);
      if (m) { userId = m[1]; break; }
    }
  }

  let lsdOk = false;
  try { require("LSD").token; lsdOk = true; } catch(e) {}
  return JSON.stringify({ userId, lsdOk, url: window.location.href });
})("USERNAME_PLACEHOLDER")
"""

# 최근 포스트 3개 fetch (collect.py JS_COLLECT 에서 first:3, maxPages:1 로 축소)
# USER_ID_PLACEHOLDER  → numeric user id string
# USERNAME_PLACEHOLDER → username string (without @)
JS_COLLECT_RECENT = r"""
(function(startCursor, maxPages) {
  const lsdToken = require("LSD").token;
  const csrf = document.cookie.match(/csrftoken=([^;]+)/);
  const csrfToken = csrf ? csrf[1] : "";
  const scripts = Array.from(document.querySelectorAll("script"));
  let hsi = null;
  for (const x of scripts) {
    if (!hsi) { const m = x.textContent.match(/"hsi":"([^"]+)"/); if (m) hsi = m[1]; }
  }

  function makeRequest(cursor) {
    const variables = JSON.stringify({
      "after": cursor || null,
      "allow_page_info_for_lox_user": true,
      "before": null,
      "first": 3,
      "last": null,
      "userID": "USER_ID_PLACEHOLDER",
      "__relay_internal__pv__BarcelonaIsLoggedInrelayprovider": false,
      "__relay_internal__pv__BarcelonaHasProfileSelfReplyContextrelayprovider": false,
      "__relay_internal__pv__BarcelonaThreadsWebCachingImprovementsrelayprovider": false,
      "__relay_internal__pv__BarcelonaHasDearAlgoConsumptionrelayprovider": true,
      "__relay_internal__pv__BarcelonaHasEventBadgerelayprovider": false,
      "__relay_internal__pv__BarcelonaIsSearchDiscoveryEnabledrelayprovider": false,
      "__relay_internal__pv__BarcelonaHasCommunitiesrelayprovider": true,
      "__relay_internal__pv__BarcelonaHasGameScoreSharerelayprovider": true,
      "__relay_internal__pv__BarcelonaHasPublicViewCountCardrelayprovider": true,
      "__relay_internal__pv__BarcelonaHasCommunityEntityCardrelayprovider": false,
      "__relay_internal__pv__BarcelonaHasScorecardCommunityrelayprovider": false,
      "__relay_internal__pv__BarcelonaHasMusicrelayprovider": false,
      "__relay_internal__pv__BarcelonaHasMessagingrelayprovider": false,
      "__relay_internal__pv__BarcelonaHasGhostPostEmojiActivationrelayprovider": false,
      "__relay_internal__pv__BarcelonaOptionalCookiesEnabledrelayprovider": true,
      "__relay_internal__pv__BarcelonaHasDearAlgoWebProductionrelayprovider": false,
      "__relay_internal__pv__BarcelonaIsCrawlerrelayprovider": false,
      "__relay_internal__pv__BarcelonaHasCommunityTopContributorsrelayprovider": false,
      "__relay_internal__pv__BarcelonaCanSeeSponsoredContentrelayprovider": false,
      "__relay_internal__pv__BarcelonaShouldShowFediverseM075Featuresrelayprovider": false,
      "__relay_internal__pv__BarcelonaIsInternalUserrelayprovider": false
    });
    const body = "av=0&__user=0&__a=1&__hs=20551.HCSV2%3Abarcelona_logged_out_pkg.2.1...0&dpr=2&__ccg=EXCELLENT&__rev=1036893687&__comet_req=122&__spin_b=trunk&__spin_r=1036893687&__hsi=" + encodeURIComponent(hsi || "") + "&lsd=" + encodeURIComponent(lsdToken) + "&jazoest=22312&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=BarcelonaProfileThreadsTabRefetchableDirectQuery&server_timestamps=true&variables=" + encodeURIComponent(variables) + "&doc_id=26348619898139541";
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "https://www.threads.com/graphql/query", false);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-FB-LSD", lsdToken);
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader("X-IG-App-ID", "238260118697367");
    xhr.setRequestHeader("X-ASBD-ID", "359341");
    xhr.setRequestHeader("X-FB-Friendly-Name", "BarcelonaProfileThreadsTabRefetchableDirectQuery");
    xhr.setRequestHeader("X-BLOKS-VERSION-ID", "86eaac606b7c5e9b45f4357f86082d05eace8411e43d3f754d885bf54a759a71");
    xhr.setRequestHeader("X-LOGGED-OUT-THREADS-MIGRATED-REQUEST", "true");
    xhr.setRequestHeader("X-Root-Field-Name", "xdt_api__v1__text_feed__user_id__profile__connection");
    xhr.send(body);
    return xhr.responseText;
  }

  function parsePage(resp) {
    try {
      const data = JSON.parse(resp);
      const edges = (data.data && data.data.mediaData && data.data.mediaData.edges) || [];
      const pi = data.data && data.data.mediaData && data.data.mediaData.page_info;
      const posts = [];
      edges.forEach(function(edge) {
        const items = (edge.node && edge.node.thread_items) || [];
        const chainPosts = [];
        items.forEach(function(item) {
          const p = item.post;
          if (!p || !p.user || p.user.username !== "USERNAME_PLACEHOLDER") return;
          const frags = p.text_post_app_info && p.text_post_app_info.text_fragments && p.text_post_app_info.text_fragments.fragments;
          if (!frags) return;
          const txt = frags.map(function(f){return f.plaintext||"";}).join("").trim();
          if (txt.length > 0) chainPosts.push({pk: p.pk, text: txt, taken_at: p.taken_at});
        });
        if (chainPosts.length === 0) return;
        chainPosts.sort(function(a, b){ return parseInt(a.pk) - parseInt(b.pk); });
        const mergedText = chainPosts.map(function(p){ return p.text; }).join("\n\n");
        if (mergedText.trim().length < 20) return;
        const entry = {pk: chainPosts[0].pk, text: mergedText, taken_at: chainPosts[0].taken_at};
        posts.push(entry);
      });
      return {posts: posts, hasNext: pi ? pi.has_next_page : false, endCursor: pi ? pi.end_cursor : null};
    } catch(e) { return {posts: [], hasNext: false, endCursor: null, error: e.message}; }
  }

  const allPosts = [];
  let cursor = startCursor || null;
  let page = 0;
  while (page < (maxPages || 1)) {
    const resp = makeRequest(cursor);
    const result = parsePage(resp);
    if (result.error) break;
    allPosts.push.apply(allPosts, result.posts);
    if (!result.hasNext || !result.endCursor) break;
    cursor = result.endCursor;
    page++;
  }
  return JSON.stringify({total: allPosts.length, posts: allPosts.slice(0, 3)});
})(null, 1);
"""

# SSR 블롭에서 프로필 메타 추출 (scout-2 옵션 A)
JS_ENRICH_PROFILE = r"""
(function() {
  const scripts = Array.from(document.querySelectorAll('script[type="application/json"][data-sjs]'));
  let profileData = null;
  for (const s of scripts) {
    try {
      const text = s.textContent;
      if (text.includes('"biography"') || text.includes('"follower_count"')) {
        const bioM    = text.match(/"biography"\s*:\s*"((?:[^"\\]|\\.)*)"/);
        const follM   = text.match(/"follower_count"\s*:\s*(\d+)/);
        const privM   = text.match(/"text_post_app_is_private"\s*:\s*(true|false)/);
        const verM    = text.match(/"is_verified"\s*:\s*(true|false)/);
        const fullM   = text.match(/"full_name"\s*:\s*"((?:[^"\\]|\\.)*)"/);
        if (bioM || follM) {
          profileData = {
            bio:            bioM  ? bioM[1]              : null,
            follower_count: follM ? parseInt(follM[1])   : null,
            is_private:     privM ? privM[1] === "true"  : null,
            is_verified:    verM  ? verM[1]  === "true"  : null,
            full_name:      fullM ? fullM[1]             : null,
          };
          break;
        }
      }
    } catch(e) {}
  }
  // fallback: OpenGraph meta
  if (!profileData) {
    const ogDesc = document.querySelector('meta[property="og:description"]');
    if (ogDesc) {
      profileData = { bio: ogDesc.getAttribute("content"), follower_count: null,
                      is_private: null, is_verified: null, full_name: null };
    }
  }
  let lsdOk = false;
  try { require("LSD").token; lsdOk = true; } catch(e) {}
  const isNotFound = document.title.toLowerCase().includes("not found")
    || document.title.toLowerCase().includes("page not found");
  return JSON.stringify({ profile: profileData, lsdOk, isNotFound, url: window.location.href });
})()
"""

# 키워드로 유저 검색 (collect.py JS_GET_USERID_API 패턴 확장)
# QUERY_PLACEHOLDER → 검색어, COUNT_PLACEHOLDER → 결과 수
JS_SEARCH_USERS = r"""
(function(query, count) {
  let lsd = null;
  try { lsd = require("LSD").token; } catch(e) {}
  if (!lsd) { return JSON.stringify({ error: "LSD token not available" }); }
  const csrf = (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || "";
  const url = "https://www.threads.net/api/v1/users/search/?q=" + encodeURIComponent(query) + "&count=" + count;
  const xhr = new XMLHttpRequest();
  xhr.open("GET", url, false);
  xhr.setRequestHeader("X-FB-LSD", lsd);
  xhr.setRequestHeader("X-CSRFToken", csrf);
  xhr.setRequestHeader("X-IG-App-ID", "238260118697367");
  xhr.send();
  try {
    const data = JSON.parse(xhr.responseText);
    const users = (data.users || []).map(function(u) {
      return { username: u.username, pk: u.pk, full_name: u.full_name || null,
               is_private: u.is_private || false, is_verified: u.is_verified || false };
    });
    return JSON.stringify({ users: users, status: xhr.status, query: query });
  } catch(e) {
    return JSON.stringify({ error: e.message, status: xhr.status,
                            raw: xhr.responseText.substring(0, 300) });
  }
})("QUERY_PLACEHOLDER", COUNT_PLACEHOLDER)
"""

# 해시태그 페이지에서 포스트 작성자 목록 추출
# TAG_PLACEHOLDER → 태그명
JS_HASHTAG_AUTHORS = r"""
(function(tag) {
  // SSR 블롭에서 username/thread_author 목록 수집
  const scripts = Array.from(document.querySelectorAll('script[type="application/json"][data-sjs]'));
  const handles = new Set();
  for (const s of scripts) {
    try {
      const text = s.textContent;
      // username 필드 전체 수집
      const usernameRe = /"username"\s*:\s*"([a-zA-Z0-9_.]{2,30})"/g;
      let m;
      while ((m = usernameRe.exec(text)) !== null) {
        handles.add(m[1].toLowerCase());
      }
    } catch(e) {}
  }
  const isNotFound = document.title.toLowerCase().includes("not found")
    || document.body.innerText.includes("Page Not Found");
  const isEmpty = handles.size === 0;
  return JSON.stringify({ handles: Array.from(handles), tag, isNotFound, isEmpty,
                          url: window.location.href });
})("TAG_PLACEHOLDER")
"""


# ── Interest resolution ───────────────────────────────────────────────────────

def load_interests_from_file() -> list | None:
    if not INTEREST_FILE.exists():
        return None
    try:
        data = json.loads(INTEREST_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [str(x) for x in data]
        if isinstance(data, dict) and "interests" in data:
            return [str(x) for x in data["interests"]]
    except Exception:
        pass
    return None


def derive_interests_from_corpus() -> list:
    """기존 코퍼스에서 상위 카테고리 (slug, count) 목록 반환."""
    counts = Counter()
    for user_dir in THREADS_ROOT.iterdir():
        if not user_dir.is_dir():
            continue
        for cat in CATEGORY_SLUGS:
            cdir = user_dir / cat
            if cdir.is_dir():
                counts[cat] += sum(1 for _ in cdir.glob("*.md"))
    return counts.most_common()


def resolve_interests(cli_arg: str | None) -> tuple:
    """
    Returns (interest_slugs, source_label).
    Priority: CLI arg > .thread-collector-interests.json > auto-derived top 3.
    """
    if cli_arg:
        slugs = [s.strip() for s in cli_arg.split(",") if s.strip()]
        return slugs, "CLI --interest"

    from_file = load_interests_from_file()
    if from_file:
        return from_file, f"{INTEREST_FILE}"

    top = derive_interests_from_corpus()[:3]
    return [slug for slug, _ in top], "auto-derived from corpus (top 3)"


# ── Corpus scanning ───────────────────────────────────────────────────────────

def existing_user_handles() -> set:
    return {d.name.lower() for d in THREADS_ROOT.iterdir() if d.is_dir()}


def iter_posts():
    """Yield (filepath, source_user, category, text) for each tracked post."""
    for user_dir in sorted(THREADS_ROOT.iterdir()):
        if not user_dir.is_dir():
            continue
        source_user = user_dir.name
        for cat in CATEGORY_SLUGS:
            cdir = user_dir / cat
            if not cdir.is_dir():
                continue
            for f in sorted(cdir.glob("*.md")):
                try:
                    text = f.read_text(encoding="utf-8")
                except Exception:
                    continue
                yield f, source_user, cat, text


def extract_context(text: str, match_start: int, match_end: int, window: int = 120) -> str:
    """멘션 주변 컨텍스트 스니펫 반환."""
    start = max(0, match_start - window)
    end = min(len(text), match_end + window)
    snippet = text[start:end]
    snippet = re.sub(r"\s+", " ", snippet).strip()
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"
    return snippet


def _is_valid_handle(handle: str) -> bool:
    """버전번호/타임스탬프처럼 보이는 handle 을 제거한다."""
    if not handle or len(handle) < 2 or len(handle) > 30:
        return False
    if not re.search(r"[a-z]", handle):
        return False
    return True


def mine_corpus(existing: set) -> dict:
    """코퍼스 전체를 스캔해 @멘션 기반 Candidate dict 를 반환한다."""
    candidates: dict = {}
    for filepath, source_user, cat, text in iter_posts():
        for m in MENTION_RE.finditer(text):
            raw = m.group(1)
            handle = raw.lower().strip(".")
            if not _is_valid_handle(handle):
                continue
            if handle in existing or handle in NOISE_HANDLES:
                continue
            cand = candidates.setdefault(handle, Candidate(handle=handle))
            cand.mentions += 1
            cand.category_counts[cat] += 1
            cand.source_users.add(source_user)
            if len(cand.contexts) < 3:
                snippet = extract_context(text, m.start(), m.end())
                cand.contexts.append((source_user, snippet))
    return candidates


# ── Source: corpus ────────────────────────────────────────────────────────────

def discover_corpus(config: DiscoverConfig) -> dict:
    """기존 코퍼스 멘션 마이닝 소스. Phase 1 mine_corpus 를 플러그인 인터페이스로 래핑."""
    candidates = mine_corpus(config.existing)
    for cand in candidates.values():
        cand.discovered_via.add("corpus")
    return candidates


# ── Source: search ────────────────────────────────────────────────────────────

def discover_search(config: DiscoverConfig) -> dict:
    """
    /api/v1/users/search/ 비공식 REST 를 통해 키워드 → 유저 목록을 반환한다.
    config.queries 의 각 키워드마다 한 번씩 호출하고 결과를 합산한다.
    실패(401/403/빈 응답) 시 stderr 경고 후 빈 결과 반환 (graceful degradation).
    """
    if not config.queries:
        return {}

    # LSD 토큰 확보를 위해 threads.net 를 먼저 방문
    print("[search] threads.net 방문해 LSD 토큰 확보 중 ...", file=sys.stderr)
    _dt_browse_goto("https://www.threads.net")
    time.sleep(1.5)

    candidates: dict = {}

    for query in config.queries:
        print(f"[search] 검색 중: {query!r}", file=sys.stderr)
        js = (JS_SEARCH_USERS
              .replace("QUERY_PLACEHOLDER", query.replace('"', '\\"'))
              .replace("COUNT_PLACEHOLDER", "20"))
        try:
            out = _dt_browse_eval(js, "/tmp/_dt_search.js")
            data = _dt_parse_json(out)
        except Exception as e:
            print(f"[search] eval 실패: {e}", file=sys.stderr)
            continue

        if not data:
            print(f"[search] JSON 파싱 실패 (query={query!r})", file=sys.stderr)
            continue

        if "error" in data:
            print(f"[search] 엔드포인트 오류 (query={query!r}): {data['error']} (status={data.get('status')})",
                  file=sys.stderr)
            continue

        status = data.get("status", 0)
        if status in (401, 403):
            print(f"[search] 인증 오류 {status} (query={query!r}). 세션 쿠키를 확인하세요.", file=sys.stderr)
            continue

        users = data.get("users", [])
        print(f"[search] {len(users)}명 발견 (query={query!r})", file=sys.stderr)

        for u in users:
            handle = (u.get("username") or "").lower().strip(".")
            if not handle or not _is_valid_handle(handle):
                continue
            if handle in config.existing or handle in NOISE_HANDLES:
                continue

            if handle not in candidates:
                candidates[handle] = Candidate(handle=handle)
            cand = candidates[handle]
            cand.discovered_via.add("search")
            if query not in cand.search_queries:
                cand.search_queries.append(query)
            # enrichment 필드 미리 채우기 (search API 가 반환한 경우)
            if cand.full_name is None and u.get("full_name"):
                cand.full_name = u["full_name"]
            if cand.is_private is None:
                cand.is_private = u.get("is_private", False)
            if cand.is_verified is None:
                cand.is_verified = u.get("is_verified", False)

        time.sleep(random.uniform(1.0, 2.0))

    return candidates


# ── Source: hashtag ───────────────────────────────────────────────────────────

def discover_hashtag(config: DiscoverConfig) -> dict:
    """
    threads.net/tag/{tag} SSR 블롭을 파싱해 포스트 작성자 목록을 반환한다.
    URL 패턴 실증 실패(404 / 빈 결과) 시 stderr 경고 후 빈 dict 반환 (graceful degradation).
    """
    if not config.hashtags:
        return {}

    candidates: dict = {}

    for tag in config.hashtags:
        tag_clean = tag.lstrip("#")
        url = f"https://www.threads.net/tag/{tag_clean}"
        print(f"[hashtag] {url} 방문 중 ...", file=sys.stderr)
        try:
            _dt_browse_goto(url)
            time.sleep(2.0)  # SSR 렌더링 대기
            js = JS_HASHTAG_AUTHORS.replace("TAG_PLACEHOLDER", tag_clean.replace('"', '\\"'))
            out = _dt_browse_eval(js, "/tmp/_dt_hashtag.js")
            data = _dt_parse_json(out)
        except Exception as e:
            print(f"[hashtag] eval 실패 (tag={tag_clean!r}): {e}", file=sys.stderr)
            continue

        if not data:
            print(f"[hashtag] JSON 파싱 실패 (tag={tag_clean!r})", file=sys.stderr)
            continue

        if data.get("isNotFound"):
            print(f"[hashtag] 페이지를 찾을 수 없음 (tag={tag_clean!r}). URL 패턴 확인 필요.", file=sys.stderr)
            continue

        handles = data.get("handles", [])
        if not handles:
            print(f"[hashtag] 작성자 없음 (tag={tag_clean!r}). SSR 구조가 다를 수 있음.", file=sys.stderr)
            continue

        # 노이즈 필터링
        valid_handles = [
            h for h in handles
            if _is_valid_handle(h)
            and h not in config.existing
            and h not in NOISE_HANDLES
        ]
        print(f"[hashtag] {len(valid_handles)}명 발견 (tag={tag_clean!r})", file=sys.stderr)

        for handle in valid_handles:
            if handle not in candidates:
                candidates[handle] = Candidate(handle=handle)
            cand = candidates[handle]
            cand.discovered_via.add("hashtag")
            if tag_clean not in cand.hashtag_matches:
                cand.hashtag_matches.append(tag_clean)

        time.sleep(random.uniform(1.0, 2.0))

    return candidates


# ── Source: explore ───────────────────────────────────────────────────────────

def discover_explore(config: DiscoverConfig) -> dict:
    """
    Phase 4 stub. Threads Explore/For You 피드는 공개 리버스엔지니어링 doc_id 없음.
    m1guelpf/threads-re, junhoyeo/threads-api 에서도 personalized feed 엔드포인트 미발견.
    향후 Meta 앱 네트워크 트래픽 분석으로 /api/v1/feed/text_post_app_for_you/ 등 확인 시 구현.

    TODO(phase-4): Explore 엔드포인트 발견 후 구현.
    """
    raise NotImplementedError(
        "discover_explore 는 Phase 4 stub 입니다.\n"
        "Threads Explore/For You 피드는 공개 리버스엔지니어링 엔드포인트가 없습니다.\n"
        "현재는 --sources corpus,search,hashtag 를 사용하세요."
    )


# ── Source registry ───────────────────────────────────────────────────────────

DISCOVERY_SOURCES: dict = {
    "corpus": discover_corpus,
    "search": discover_search,
    "hashtag": discover_hashtag,
    "explore": discover_explore,
}


# ── Dedup & merge ─────────────────────────────────────────────────────────────

def merge_candidates(source_results: list) -> dict:
    """
    여러 소스에서 반환된 dict[handle, Candidate] 들을 handle 기준으로 merge.
    discovered_via set 합집합, mentions/search_queries/hashtag_matches 합산.
    """
    merged: dict = {}
    for source_name, cands in source_results:
        for handle, cand in cands.items():
            if handle not in merged:
                merged[handle] = cand
            else:
                base = merged[handle]
                # 소스 집합 합산
                base.discovered_via |= cand.discovered_via
                # corpus 멘션 누적 (search/hashtag 는 mentions=0 초기값)
                base.mentions = max(base.mentions, cand.mentions)
                base.category_counts += cand.category_counts
                base.source_users |= cand.source_users
                # contexts 는 corpus 우선 (비어 있을 때만 채움)
                if not base.contexts:
                    base.contexts = cand.contexts
                # search_queries 중복 제거 병합
                for q in cand.search_queries:
                    if q not in base.search_queries:
                        base.search_queries.append(q)
                # hashtag_matches 중복 제거 병합
                for t in cand.hashtag_matches:
                    if t not in base.hashtag_matches:
                        base.hashtag_matches.append(t)
                # explore_rank 최소값 유지
                if cand.explore_rank is not None:
                    base.explore_rank = (
                        min(base.explore_rank, cand.explore_rank)
                        if base.explore_rank is not None else cand.explore_rank
                    )
                # search API 가 반환한 프로필 정보 채우기
                if base.full_name is None and cand.full_name:
                    base.full_name = cand.full_name
                if base.is_private is None and cand.is_private is not None:
                    base.is_private = cand.is_private
                if base.is_verified is None and cand.is_verified is not None:
                    base.is_verified = cand.is_verified
    return merged


# ── Enrich ────────────────────────────────────────────────────────────────────

def _fetch_recent_posts(handle: str, user_id: str) -> list:
    """
    JS_COLLECT_RECENT (first:3, maxPages:1) 로 최근 포스트 최대 3개를 가져온다.
    프로필 페이지에 이미 goto 된 상태이므로 추가 goto 불필요.
    실패 시 빈 리스트 반환 (graceful).
    """
    js = (
        JS_COLLECT_RECENT
        .replace("USER_ID_PLACEHOLDER", user_id)
        .replace("USERNAME_PLACEHOLDER", handle)
    )
    try:
        out = _dt_browse_eval(js, f"/tmp/_dt_recent_{handle}.js")
        data = _dt_parse_json(out)
    except Exception as e:
        print(f"[enrich] {handle}: 최근 포스트 fetch 오류 — {e}", file=sys.stderr)
        return []

    if not data:
        print(f"[enrich] {handle}: 최근 포스트 JSON 파싱 실패", file=sys.stderr)
        return []

    posts_raw = data.get("posts", [])
    result = []
    for p in posts_raw[:3]:
        text = str(p.get("text", "")).strip()
        taken_at = p.get("taken_at")
        if text:
            result.append({"text": text, "taken_at": taken_at})
    return result


def enrich_candidate(cand: Candidate) -> None:
    """
    scout-2 옵션 A: SSR JSON blob 에서 프로필 메타를 추출해 cand 에 채운다.
    프로필 메타 성공 후 JS_COLLECT_RECENT 로 최근 포스트 3개도 채운다.
    실패해도 cand 를 제거하지 않고 enrich_status 로 표기한다.
    recent_posts fetch 실패 시 bio/follower 등 다른 필드는 유지하고
    enrich_status 는 "success" 를 그대로 둔다 (부분 성공).
    """
    url = f"https://www.threads.net/@{cand.handle}"
    try:
        _dt_browse_goto(url)
        time.sleep(1.0)  # SSR 렌더링 대기
        out = _dt_browse_eval(JS_ENRICH_PROFILE, f"/tmp/_dt_enrich_{cand.handle}.js")
        data = _dt_parse_json(out)
    except Exception as e:
        print(f"[enrich] {cand.handle}: 실행 오류 — {e}", file=sys.stderr)
        cand.enrich_status = "failed"
        return

    if not data:
        print(f"[enrich] {cand.handle}: JSON 파싱 실패", file=sys.stderr)
        cand.enrich_status = "failed"
        return

    # LSD 토큰 미준비 시 한 번 재시도
    if not data.get("lsdOk"):
        print(f"[enrich] {cand.handle}: LSD 미준비, 재시도 ...", file=sys.stderr)
        _dt_browse_goto(url)
        time.sleep(1.5)
        out = _dt_browse_eval(JS_ENRICH_PROFILE, f"/tmp/_dt_enrich_{cand.handle}.js")
        data = _dt_parse_json(out) or {}

    if data.get("isNotFound"):
        print(f"[enrich] {cand.handle}: 페이지 없음 (404)", file=sys.stderr)
        cand.enrich_status = "failed"
        return

    profile = data.get("profile")
    if not profile:
        print(f"[enrich] {cand.handle}: 프로필 데이터 없음", file=sys.stderr)
        cand.enrich_status = "failed"
        return

    # 비공개 계정
    if profile.get("is_private"):
        cand.is_private = True
        cand.enrich_status = "private"
        print(f"[enrich] {cand.handle}: 비공개 계정", file=sys.stderr)
        return

    # 필드 채우기 (SSR 블롭에서 추출한 문자열은 \uXXXX 리터럴이 남을 수 있으므로 디코딩)
    cand.bio = _decode_unicode_escapes(profile.get("bio"))
    cand.follower_count = profile.get("follower_count")
    cand.is_private = profile.get("is_private")
    cand.is_verified = profile.get("is_verified")
    if cand.full_name is None:
        cand.full_name = _decode_unicode_escapes(profile.get("full_name"))
    cand.enrich_status = "success"
    print(f"[enrich] {cand.handle}: 프로필 완료 (팔로워={cand.follower_count})", file=sys.stderr)

    # 최근 포스트 3개 fetch — userID 먼저 확보 (이미 프로필 페이지에 있으므로 goto 불필요)
    js_uid = JS_GET_USERID_DT.replace("USERNAME_PLACEHOLDER", cand.handle)
    try:
        uid_out = _dt_browse_eval(js_uid, f"/tmp/_dt_uid_{cand.handle}.js")
        uid_data = _dt_parse_json(uid_out)
        user_id = uid_data.get("userId") if uid_data else None
    except Exception as e:
        print(f"[enrich] {cand.handle}: userID 추출 오류 — {e}", file=sys.stderr)
        user_id = None

    if user_id:
        print(f"[enrich] {cand.handle}: userID={user_id}, 최근 포스트 fetch 중 ...", file=sys.stderr)
        posts = _fetch_recent_posts(cand.handle, user_id)
        cand.recent_posts = posts
        print(f"[enrich] {cand.handle}: 최근 포스트 {len(posts)}개 수집", file=sys.stderr)
    else:
        print(f"[enrich] {cand.handle}: userID 없음, 최근 포스트 skip (recent_posts=[])", file=sys.stderr)


# ── Ranking ───────────────────────────────────────────────────────────────────

def score_candidates(candidates: dict, config: DiscoverConfig) -> None:
    """
    소스별 가중치 합산으로 최종 score 를 계산한다.
    Phase 1 단독 호출 시 corpus 점수만 계산되어 기존 공식과 동일한 상대 순위를 유지.
    """
    interest_set = set(config.interests)
    w = config.weights

    for cand in candidates.values():
        # corpus 점수 (기존 Phase 1 공식 유지)
        corpus_score = 0.0
        if "corpus" in cand.discovered_via and cand.mentions > 0:
            in_topic = sum(n for cat, n in cand.category_counts.items() if cat in interest_set)
            ratio = in_topic / cand.mentions
            diversity = min(len(cand.source_users), 3) / 3
            corpus_score = cand.mentions * (1 + ratio) * (0.5 + 0.5 * diversity)

        # search 점수
        search_score = 0.0
        if "search" in cand.discovered_via:
            search_score = len(cand.search_queries) * 2.0

        # hashtag 점수
        hashtag_score = 0.0
        if "hashtag" in cand.discovered_via:
            hashtag_score = len(cand.hashtag_matches) * 1.5

        # explore 점수
        explore_score = 0.0
        if "explore" in cand.discovered_via and cand.explore_rank:
            explore_score = 1.0 / cand.explore_rank

        # enrichment 부스트 (follower count 로그 스케일)
        enrich_boost = 1.0
        if cand.enrich_status == "success" and cand.follower_count:
            enrich_boost = 1.0 + math.log10(max(cand.follower_count, 1)) / 10.0

        cand.score = (
            w.get("corpus", 3.0) * corpus_score
            + w.get("search", 1.0) * search_score
            + w.get("hashtag", 1.0) * hashtag_score
            + w.get("explore", 2.0) * explore_score
        ) * enrich_boost


# ── Markdown report ───────────────────────────────────────────────────────────

def render_report(
    candidates: list,
    config: DiscoverConfig,
    interest_source: str,
    total_posts: int,
    total_users: int,
) -> str:
    today = date.today().isoformat()
    active_sources = ", ".join(config.sources)

    lines = [
        f"# Threads 후보 유저 발견 — {today}",
        "",
        "> 기존 코퍼스에서 @멘션된 아직 수집 안 된 유저 목록입니다.",
        "> 링크를 클릭해 프로필을 훑어본 뒤 괜찮은 유저는 `/collect @handle` 로 수집하세요.",
        "",
        "## 스캔 결과",
        "",
        f"- 소스: **{active_sources}**",
        f"- 분석 대상: **{total_posts}** 개 포스트, **{total_users}** 명 유저",
        f"- 관심사: **{', '.join(config.interests) if config.interests else '(없음)'}** ({interest_source})",
        f"- 필터: 멘션 {config.min_mentions}회 이상 (corpus 소스에만 적용)",
        f"- 후보 수: **{len(candidates)}** 명",
    ]

    if config.queries:
        lines.append(f"- 검색 쿼리: {', '.join(repr(q) for q in config.queries)}")
    if config.hashtags:
        lines.append(f"- 해시태그: {', '.join('#' + t for t in config.hashtags)}")

    lines += ["", "---", ""]

    if not candidates:
        lines.append("> 조건을 만족하는 후보가 없습니다. `--min-mentions 1` 또는 `--sources` 를 추가해 보세요.")
        return "\n".join(lines)

    for i, cand in enumerate(candidates, 1):
        top_cats = cand.category_counts.most_common(3)
        cat_label = ", ".join(f"{c} ({n})" for c, n in top_cats) if top_cats else "(없음)"
        src_label = ", ".join(f"@{u}" for u in sorted(cand.source_users)) if cand.source_users else "(없음)"

        lines.append(f"## {i}. @{cand.handle}")
        lines.append("")
        lines.append(f"- [프로필 열기](https://www.threads.net/@{cand.handle})")
        lines.append(f"- **멘션 수**: {cand.mentions}회")

        if top_cats:
            lines.append(f"- **주요 카테고리**: {cat_label}")
        if cand.source_users:
            lines.append(f"- **언급한 유저**: {src_label}")
        lines.append(f"- **점수**: {cand.score:.2f}")

        # 소스 배지
        via_sorted = sorted(cand.discovered_via)
        via_badges = []
        for v in via_sorted:
            if v == "search" and cand.search_queries:
                via_badges.append(f'[search: {", ".join(repr(q) for q in cand.search_queries)}]')
            elif v == "hashtag" and cand.hashtag_matches:
                via_badges.append(f'[hashtag: {", ".join("#" + t for t in cand.hashtag_matches)}]')
            else:
                via_badges.append(f"[{v}]")
        if via_badges:
            lines.append(f"- **소스**: {' '.join(via_badges)}")

        # enrichment 섹션
        if cand.enrich_status == "success":
            if cand.full_name:
                lines.append(f"- **이름**: {cand.full_name}")
            if cand.is_verified:
                lines.append("- **인증 계정**: ✓")
            if cand.follower_count is not None:
                lines.append(f"- **팔로워**: {cand.follower_count:,}명")
            if cand.bio:
                lines.append(f"- **소개**: {cand.bio[:120]}")
            if cand.recent_posts:
                lines.append("")
                lines.append("**최근 포스트:**")
                for p in cand.recent_posts[:3]:
                    snippet = str(p.get("text", ""))[:120]
                    lines.append(f"> {snippet}")
        elif cand.enrich_status == "private":
            lines.append("- **계정 상태**: 🔒 비공개 계정")
        elif cand.enrich_status == "failed":
            lines.append("- **계정 상태**: ⚠️ enrich 실패 (수동 확인 필요)")
        elif cand.enrich_status == "skipped":
            # enrich 미실행 시 search API 가 반환한 메타 출력
            if cand.full_name:
                lines.append(f"- **이름**: {cand.full_name}")
            if cand.is_verified:
                lines.append("- **인증 계정**: ✓")

        # corpus 컨텍스트
        if cand.contexts:
            lines.append("")
            lines.append("**멘션 컨텍스트**:")
            lines.append("")
            for src, snippet in cand.contexts:
                lines.append(f"> *@{src}*: {snippet}")
                lines.append(">")

        lines.append("")
        lines.append(f"**다음 단계**: 프로필 확인 후 괜찮으면 → `/collect @{cand.handle}`")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_weights(raw: str) -> dict:
    """'corpus:3,search:1,hashtag:1' 형태 문자열을 dict 로 파싱한다."""
    result = {}
    for pair in raw.split(","):
        pair = pair.strip()
        if ":" not in pair:
            continue
        key, val = pair.split(":", 1)
        try:
            result[key.strip()] = float(val.strip())
        except ValueError:
            pass
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Discover candidate Threads users via corpus mention mining, search, and hashtag pages."
    )
    # Phase 1 기존 인자 (유지)
    ap.add_argument("--interest", help="Comma-separated category slugs (overrides interest file and auto-derivation)")
    ap.add_argument("--limit", type=int, default=20, help="Max candidates in the report (default 20)")
    ap.add_argument("--min-mentions", type=int, default=2, help="Minimum mention count for corpus source (default 2)")
    ap.add_argument("--output", help="Output markdown path (default .claude/discover-threads/YYYYMMDD-candidates.md)")
    ap.add_argument("--print", action="store_true", help="Also print report to stdout")
    # Phase 2+ 신규 인자
    ap.add_argument("--enrich", action="store_true", default=False,
                    help="Enrich candidates with profile bio/follower count via SSR parsing (slow, opt-in)")
    ap.add_argument("--enrich-limit", type=int, default=10,
                    help="Max candidates to enrich (default 10, to save time)")
    ap.add_argument("--sources", default="corpus",
                    help="Comma-separated discovery sources: corpus,search,hashtag,explore (default: corpus)")
    ap.add_argument("--query", action="append", default=[],
                    help="Search keyword (repeatable: --query 'AI 수익화' --query '바이브코딩')")
    ap.add_argument("--hashtag", action="append", default=[],
                    help="Hashtag to scrape (repeatable: --hashtag ai_llm --hashtag vibe_coding)")
    ap.add_argument("--weights", default=None,
                    help="Score weights, e.g. 'corpus:3,search:1,hashtag:1' (default: corpus:3,search:1,hashtag:1,explore:2)")
    args = ap.parse_args()

    if not THREADS_ROOT.is_dir():
        sys.exit(f"No {THREADS_ROOT}/ directory found. Run from repo root.")

    existing = existing_user_handles()
    total_users = len(existing)
    interests, interest_source = resolve_interests(args.interest)

    # 가중치 파싱
    default_weights = {"corpus": 3.0, "search": 1.0, "hashtag": 1.0, "explore": 2.0}
    weights = {**default_weights, **(parse_weights(args.weights) if args.weights else {})}

    # 소스 목록 파싱
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    unknown = set(sources) - set(DISCOVERY_SOURCES)
    if unknown:
        sys.exit(f"알 수 없는 소스: {', '.join(sorted(unknown))}. 가능한 소스: {', '.join(DISCOVERY_SOURCES)}")

    config = DiscoverConfig(
        sources=sources,
        interests=interests,
        existing=existing,
        enrich=args.enrich,
        queries=args.query or [],
        hashtags=args.hashtag or [],
        min_mentions=args.min_mentions,
        limit=args.limit,
        enrich_limit=args.enrich_limit,
        weights=weights,
    )

    # 소스별 discover 실행 + merge
    source_results = []
    for src in sources:
        fn = DISCOVERY_SOURCES[src]
        print(f"[discover] 소스 실행: {src}", file=sys.stderr)
        try:
            result = fn(config)
            source_results.append((src, result))
            print(f"[discover] {src}: {len(result)}명 발견", file=sys.stderr)
        except NotImplementedError as e:
            print(f"[discover] {src}: {e}", file=sys.stderr)
            # explore 같은 stub 는 경고 후 스킵
            continue
        except Exception as e:
            print(f"[discover] {src}: 오류 발생 — {e}", file=sys.stderr)
            continue

    candidates_map = merge_candidates(source_results)

    # corpus min_mentions 필터 (corpus 소스가 있는 경우에만)
    if "corpus" in sources:
        candidates_map = {
            h: c for h, c in candidates_map.items()
            if "corpus" not in c.discovered_via or c.mentions >= config.min_mentions
        }

    # 총 포스트 수 계산 (corpus 소스가 있을 때만)
    total_posts = sum(1 for _ in iter_posts()) if "corpus" in sources else 0

    # 점수 계산
    score_candidates(candidates_map, config)
    ranked = sorted(candidates_map.values(), key=lambda c: c.score, reverse=True)[: args.limit]

    # Enrichment (opt-in)
    if args.enrich and ranked:
        print(f"[enrich] 상위 {min(args.enrich_limit, len(ranked))}명 enrichment 시작 ...", file=sys.stderr)
        for cand in ranked[: args.enrich_limit]:
            enrich_candidate(cand)
            time.sleep(random.uniform(1.0, 2.0))
        # enrich 후 재점수 (follower 부스트 반영)
        score_candidates(candidates_map, config)
        ranked = sorted(candidates_map.values(), key=lambda c: c.score, reverse=True)[: args.limit]

    report = render_report(
        ranked,
        config=config,
        interest_source=interest_source,
        total_posts=total_posts,
        total_users=total_users,
    )

    out_path = (
        Path(args.output)
        if args.output
        else OUTPUT_ROOT / f"{date.today().strftime('%Y%m%d')}-candidates.md"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    print(f"DiscoverThreads done — {len(ranked)} candidates")
    print(f"  Sources:   {', '.join(sources)}")
    print(f"  Interests: {', '.join(interests)}  ({interest_source})")
    if "corpus" in sources:
        print(f"  Scanned:   {total_posts} posts from {total_users} users")
    print(f"  Report:    {out_path}")
    if ranked:
        print(f"\n  Top 5 by score:")
        for c in ranked[:5]:
            via = "+".join(sorted(c.discovered_via))
            print(f"    {c.score:5.2f}  @{c.handle:25s}  ({c.mentions} mentions, "
                  f"src={via}, enrich={c.enrich_status})")

    if args.print:
        print()
        print(report)


if __name__ == "__main__":
    main()
