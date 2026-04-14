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


# ── Ranking ───────────────────────────────────────────────────────────────────

def score_candidates(candidates: dict, interests: list) -> None:
    """
    Score = mentions * (1 + topic_match_ratio).
    topic_match_ratio = fraction of mentions that occurred in interest categories.
    Also boost by source-user diversity (prevents one user's inside jokes).
    """
    interest_set = set(interests)
    for cand in candidates.values():
        in_topic = sum(n for cat, n in cand.category_counts.items() if cat in interest_set)
        ratio = in_topic / cand.mentions if cand.mentions else 0
        diversity = min(len(cand.source_users), 3) / 3  # cap at 3 unique mentioners
        cand.score = cand.mentions * (1 + ratio) * (0.5 + 0.5 * diversity)


# ── Markdown report ───────────────────────────────────────────────────────────

def render_report(
    candidates: list,
    interests: list,
    interest_source: str,
    total_posts: int,
    total_users: int,
    min_mentions: int,
) -> str:
    today = date.today().isoformat()
    lines = [
        f"# Threads 후보 유저 발견 — {today}",
        "",
        "> 기존 코퍼스에서 @멘션된 아직 수집 안 된 유저 목록입니다.",
        "> 링크를 클릭해 프로필을 훑어본 뒤 괜찮은 유저는 `/collect @handle` 로 수집하세요.",
        "",
        "## 스캔 결과",
        "",
        f"- 스캔 소스: 기존 코퍼스 멘션 마이닝 (`{THREADS_ROOT}/`)",
        f"- 분석 대상: **{total_posts}** 개 포스트, **{total_users}** 명 유저",
        f"- 관심사: **{', '.join(interests) if interests else '(없음)'}** ({interest_source})",
        f"- 필터: 멘션 {min_mentions}회 이상",
        f"- 후보 수: **{len(candidates)}** 명",
        "",
        "---",
        "",
    ]

    if not candidates:
        lines.append("> 멘션 조건을 만족하는 후보가 없습니다. `--min-mentions 1` 로 다시 실행해 보세요.")
        return "\n".join(lines)

    for i, cand in enumerate(candidates, 1):
        top_cats = cand.category_counts.most_common(3)
        cat_label = ", ".join(f"{c} ({n})" for c, n in top_cats)
        src_label = ", ".join(f"@{u}" for u in sorted(cand.source_users))

        lines.append(f"## {i}. @{cand.handle}")
        lines.append("")
        lines.append(f"- [프로필 열기](https://www.threads.net/@{cand.handle})")
        lines.append(f"- **멘션 수**: {cand.mentions}회")
        lines.append(f"- **주요 카테고리**: {cat_label}")
        lines.append(f"- **언급한 유저**: {src_label}")
        lines.append(f"- **점수**: {cand.score:.2f}")
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

def main() -> None:
    ap = argparse.ArgumentParser(description="Discover candidate Threads users via corpus mention mining.")
    ap.add_argument("--interest", help="Comma-separated category slugs (overrides interest file and auto-derivation)")
    ap.add_argument("--limit", type=int, default=20, help="Max candidates in the report (default 20)")
    ap.add_argument("--min-mentions", type=int, default=2, help="Minimum mention count (default 2)")
    ap.add_argument("--output", help="Output markdown path (default .claude/discover-threads/YYYYMMDD-candidates.md)")
    ap.add_argument("--print", action="store_true", help="Also print report to stdout")
    args = ap.parse_args()

    if not THREADS_ROOT.is_dir():
        sys.exit(f"No {THREADS_ROOT}/ directory found. Run from repo root.")

    existing = existing_user_handles()
    total_users = len(existing)

    interests, source = resolve_interests(args.interest)

    candidates_map = mine_corpus(existing)
    total_posts = sum(1 for _ in iter_posts())

    filtered = [c for c in candidates_map.values() if c.mentions >= args.min_mentions]
    score_candidates({c.handle: c for c in filtered}, interests)
    ranked = sorted(filtered, key=lambda c: c.score, reverse=True)[: args.limit]

    report = render_report(
        ranked,
        interests=interests,
        interest_source=source,
        total_posts=total_posts,
        total_users=total_users,
        min_mentions=args.min_mentions,
    )

    out_path = Path(args.output) if args.output else OUTPUT_ROOT / f"{date.today().strftime('%Y%m%d')}-candidates.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    print(f"DiscoverThreads done — {len(ranked)} candidates")
    print(f"  Interests: {', '.join(interests)}  ({source})")
    print(f"  Scanned:   {total_posts} posts from {total_users} users")
    print(f"  Report:    {out_path}")
    if ranked:
        print(f"\n  Top 5 by score:")
        for c in ranked[:5]:
            print(f"    {c.score:5.2f}  @{c.handle:25s}  ({c.mentions} mentions, "
                  f"from {len(c.source_users)} users)")

    if args.print:
        print()
        print(report)


if __name__ == "__main__":
    main()
