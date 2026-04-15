#!/usr/bin/env python3
"""
ThreadCollector — standalone collect script
Usage: python3 -m sources.threads.collect @username [--limit 20] [--types tech,product,career]

Collects Threads.net posts via GraphQL pagination using the browse binary,
classifies them into categories, and saves individual markdown files.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# repo 루트를 sys.path에 추가 (직접 실행 및 -m 호출 모두 지원)
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# ── Constants ─────────────────────────────────────────────────────────────────

BROWSE_BIN = os.path.expanduser("~/.claude/skills/gstack/browse/dist/browse")
BROWSE_SRC = os.path.expanduser("~/.claude/skills/gstack/browse/src/cli.ts")
BROWSE_CMD: list[str] = []  # resolved at startup

CATEGORY_LABELS = {
    "ai-llm": "AI/LLM",
    "viral-sns": "바이럴/SNS/마케팅",
    "monetization": "수익화/부수입",
    "dev-tools": "개발도구/스택",
    "product-strategy": "제품전략/PMF",
    "startup-philosophy": "창업철학/인디해킹",
    "career-growth": "커리어/성장",
    "learning-retro": "학습/회고",
    "productivity": "생산성/워크플로우",
    "web-app": "웹/앱 개발",
    # 신규 3개 (2026-04-15)
    "portfolio-ops": "포트폴리오 운영",
    "aso": "ASO/출시전략",
    "case-study": "사례연구",
    "uncategorized": "미분류",
}

TECH_KEYWORDS = [
    "개발", "코드", "코딩", "프로그래밍", "구현", "배포", "아키텍처", "설계",
    "api", "sdk", "라이브러리", "프레임워크", "데이터베이스", "db", "서버",
    "ios", "android", "앱", "app", "모바일", "swift", "kotlin", "flutter",
    "react", "vue", "angular", "typescript", "javascript", "python", "java",
    "supabase", "firebase", "aws", "gcp", "azure", "클라우드",
    "ai", "인공지능", "llm", "gpt", "claude", "gemini", "머신러닝", "ml",
    "프롬프트", "prompt", "모델", "rag", "embedding", "벡터",
    "git", "테스트", "ci/cd", "디버깅", "버그", "에러", "최적화", "성능", "보안",
    "saas", "마이크로서비스", "캐싱", "쿼리", "비동기", "async",
]

PRODUCT_KEYWORDS = [
    "제품", "프로덕트", "product", "pmf", "시장", "마켓", "market",
    "고객", "유저", "사용자", "피드백", "기능", "피처", "출시", "런칭",
    "스타트업", "창업", "투자", "펀딩", "매출", "수익", "영업", "마케팅",
    "브랜드", "포지셔닝", "경쟁", "차별화", "성장", "growth", "kpi", "okr",
]

CAREER_KEYWORDS = [
    "커리어", "직장", "이직", "취업", "면접", "팀", "동료", "리더십",
    "성장", "배움", "공부", "학습", "독서", "책", "실패", "경험", "인사이트", "회고",
    "생산성", "집중", "습관", "루틴", "번아웃", "인생", "삶", "목표", "동기",
    "커뮤니티", "글쓰기", "개발자", "엔지니어",
]

# ── JavaScript templates ───────────────────────────────────────────────────────

JS_GET_USERID = r"""
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

JS_GET_USERID_API = r"""
(function(username) {
  const lsd = require("LSD").token;
  const csrf = (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || "";
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "https://www.threads.net/api/v1/users/search/?q=" + username + "&count=1", false);
  xhr.setRequestHeader("X-FB-LSD", lsd);
  xhr.setRequestHeader("X-CSRFToken", csrf);
  xhr.setRequestHeader("X-IG-App-ID", "238260118697367");
  xhr.send();
  try {
    const data = JSON.parse(xhr.responseText);
    const users = data.users || [];
    const match = users.find(function(u) { return u.username === username; });
    return JSON.stringify({ userId: match ? match.pk : null, status: xhr.status });
  } catch(e) {
    return JSON.stringify({ error: e.message, raw: xhr.responseText.substring(0, 200) });
  }
})("USERNAME_PLACEHOLDER")
"""

# The main pagination collector script. Placeholders:
#   USER_ID_PLACEHOLDER  → numeric user id string
#   USERNAME_PLACEHOLDER → username string (without @)
#   CURSOR_PLACEHOLDER   → JSON cursor value (null or "string")
#   PAGES_PLACEHOLDER    → integer (number of pages per batch call)
JS_COLLECT = r"""
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
      "first": 11,
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
        // Each edge is one Thread (chain). Collect ALL posts by the target user
        // within this edge — including is_reply:true continuations.
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
        // Sort chronologically by pk (ascending = oldest first)
        chainPosts.sort(function(a, b){ return parseInt(a.pk) - parseInt(b.pk); });
        const mergedText = chainPosts.map(function(p){ return p.text; }).join("\n\n");
        if (mergedText.trim().length < 20) return;
        const entry = {pk: chainPosts[0].pk, text: mergedText, taken_at: chainPosts[0].taken_at};
        if (chainPosts.length > 1) entry.chain_pks = chainPosts.map(function(p){ return p.pk; });
        posts.push(entry);
      });
      return {posts: posts, hasNext: pi ? pi.has_next_page : false, endCursor: pi ? pi.end_cursor : null};
    } catch(e) { return {posts: [], hasNext: false, endCursor: null, error: e.message}; }
  }

  const allPosts = [];
  let cursor = startCursor || null;
  let page = 0;
  let finalCursor = null;
  while (page < (maxPages || 5)) {
    const resp = makeRequest(cursor);
    const result = parsePage(resp);
    if (result.error) break;
    allPosts.push.apply(allPosts, result.posts);
    finalCursor = result.endCursor;
    if (!result.hasNext || !result.endCursor) { finalCursor = null; break; }
    cursor = result.endCursor;
    page++;
  }
  return JSON.stringify({total: allPosts.length, pages: page+1, nextCursor: finalCursor, posts: allPosts});
})(CURSOR_PLACEHOLDER, PAGES_PLACEHOLDER);
"""

# ── Browse helpers ─────────────────────────────────────────────────────────────

# Chrome profile paths to search (in priority order)
CHROME_PROFILE_PATHS = [
    "~/Library/Application Support/Google/Chrome/Profile 7/Cookies",
    "~/Library/Application Support/Google/Chrome/Default/Cookies",
    "~/Library/Application Support/Chromium/Default/Cookies",
    "~/.config/google-chrome/Default/Cookies",
]

THREADS_COOKIE_URL = "https://threads.com"


def _resolve_browse_cmd() -> list[str]:
    """Determine how to invoke the browse CLI.

    1. Try the compiled binary — run a quick ``--help`` to verify macOS
       doesn't SIGKILL it (exit 137 = unsigned binary on Apple Silicon).
    2. If that fails and ``bun`` + the source .ts file exist, fall back to
       ``bun run <cli.ts>``.
    3. Otherwise return the binary path anyway (will fail later with a clear
       error).
    """
    if os.path.isfile(BROWSE_BIN) and os.access(BROWSE_BIN, os.X_OK):
        try:
            r = subprocess.run(
                [BROWSE_BIN, "--help"],
                capture_output=True, timeout=5,
            )
            if r.returncode not in (137, -9):  # not killed by macOS
                return [BROWSE_BIN]
        except Exception:
            pass

    # Fallback: bun run <source>
    bun = os.path.expanduser("~/.bun/bin/bun")
    if not os.path.isfile(bun):
        import shutil
        bun = shutil.which("bun") or bun
    if os.path.isfile(bun) and os.path.isfile(BROWSE_SRC):
        print("[browse] compiled binary unavailable — using bun runtime fallback")
        return [bun, "run", BROWSE_SRC]

    return [BROWSE_BIN]


def _browse_run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a browse sub-command using the resolved BROWSE_CMD."""
    return subprocess.run(BROWSE_CMD + args, **kwargs)


def inject_chrome_cookies() -> None:
    """
    Extract Threads session cookies from the user's Chrome profile and inject
    them into the browse session via `$B cookie n=v`. Best-effort: silently
    skips if pycookiecheat is not installed or no Chrome profile is found.
    """
    try:
        import pycookiecheat  # type: ignore
    except ImportError:
        return  # Optional dependency; skip silently

    cookie_file = None
    for raw_path in CHROME_PROFILE_PATHS:
        p = os.path.expanduser(raw_path)
        if os.path.isfile(p):
            cookie_file = p
            break

    if not cookie_file:
        return

    try:
        cookies: dict = pycookiecheat.chrome_cookies(
            THREADS_COOKIE_URL, cookie_file=cookie_file
        )
    except Exception:
        return

    if not cookies:
        return

    print(f"[0/5] Injecting {len(cookies)} Chrome session cookies ...")
    # Navigate to threads.net first so browse has a page context for cookie domain
    _browse_run(["goto", "https://www.threads.net"], capture_output=True, timeout=30)
    for name, value in cookies.items():
        _browse_run(
            ["cookie", f"{name}={value}"],
            capture_output=True, timeout=10,
        )


def browse_goto(url: str) -> None:
    """Navigate the browse browser to a URL (fire-and-forget, no long wait)."""
    _browse_run(["goto", url], capture_output=True, timeout=30)


def browse_eval(js: str, tmp_path: str = "/tmp/_tc_eval.js") -> str:
    """Write js to a temp file and eval it via browse, returning stdout+stderr."""
    with open(tmp_path, "w") as fh:
        fh.write(js)
    result = _browse_run(
        ["eval", tmp_path],
        capture_output=True, text=True, timeout=120,
    )
    return (result.stdout + result.stderr).strip()


def parse_json_output(output: str) -> dict | None:
    """Find the first JSON object line in browse eval output."""
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                pass
    return None

# ── Step: get user ID ─────────────────────────────────────────────────────────

def get_user_id(username: str) -> str:
    profile_url = f"https://www.threads.net/@{username}"

    print(f"[1/5] Navigating to {profile_url} ...")
    browse_goto(profile_url)

    # Primary: extract from page scripts (username-aware)
    print("[1/5] Extracting userID from page scripts ...")
    js_userid = JS_GET_USERID.replace("USERNAME_PLACEHOLDER", username)
    out = browse_eval(js_userid, f"/tmp/_tc_userid_{username}.js")
    data = parse_json_output(out)

    if data and data.get("userId"):
        print(f"[1/5] userID = {data['userId']}")
        return data["userId"]

    # If lsdOk is False, try reloading once
    if data and not data.get("lsdOk"):
        print("[1/5] LSD not ready, retrying goto ...")
        browse_goto(profile_url)
        out = browse_eval(js_userid, f"/tmp/_tc_userid_{username}.js")
        data = parse_json_output(out)
        if data and data.get("userId"):
            print(f"[1/5] userID = {data['userId']}")
            return data["userId"]

    # Fallback: search API
    print("[1/5] Falling back to search API for userID ...")
    js_api = JS_GET_USERID_API.replace("USERNAME_PLACEHOLDER", username)
    out = browse_eval(js_api, f"/tmp/_tc_userid_api_{username}.js")
    data = parse_json_output(out)
    if data and data.get("userId"):
        print(f"[1/5] userID (from API) = {data['userId']}")
        return data["userId"]

    sys.exit(
        f"ERROR: Could not determine userID for @{username}.\n"
        "Please check that the username is correct and that browse has a valid session.\n"
        "You can also pass the userID directly via --user-id <ID>."
    )

# ── Step: collect posts ────────────────────────────────────────────────────────

def build_collect_script(user_id: str, username: str) -> str:
    """Return the JS collection template with user_id and username substituted."""
    return (
        JS_COLLECT
        .replace("USER_ID_PLACEHOLDER", user_id)
        .replace("USERNAME_PLACEHOLDER", username)
    )


def run_batch(script_template: str, cursor: str | None, pages_per_batch: int = 5) -> dict | None:
    """Run one collect batch; returns parsed JSON or None on failure."""
    cursor_js = json.dumps(cursor)  # null or "string"
    # Replace the IIFE tail: (CURSOR_PLACEHOLDER, PAGES_PLACEHOLDER);
    script = script_template.replace("CURSOR_PLACEHOLDER", cursor_js).replace(
        "PAGES_PLACEHOLDER", str(pages_per_batch)
    )
    out = browse_eval(script, "/tmp/_tc_batch.js")
    for line in out.splitlines():
        line = line.strip()
        if line.startswith('{"total"') or line.startswith('{"posts"'):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                pass
    return None


def collect_posts(username: str, user_id: str, limit: int) -> list[dict]:
    """
    Paginate through all batches up to `limit` and return raw post list.
    Each post: {pk, text, taken_at}
    """
    profile_url = f"https://www.threads.net/@{username}"
    script_template = build_collect_script(user_id, username)

    all_posts: list[dict] = []
    seen_pks: set[str] = set()
    cursor: str | None = None
    fails = 0

    print(f"[2/5] Starting collection (max {limit} batches) ...")
    browse_goto(profile_url)

    for batch_idx in range(limit):
        result = run_batch(script_template, cursor)
        if result is None:
            fails += 1
            print(f"  Batch {batch_idx + 1}: no result (fail {fails}/3)")
            if fails >= 3:
                print("  Too many consecutive failures, stopping.")
                break
            browse_goto(profile_url)
            continue

        fails = 0
        new_posts = [p for p in result.get("posts", []) if p["pk"] not in seen_pks]
        for p in new_posts:
            seen_pks.add(p["pk"])
        all_posts.extend(new_posts)
        cursor = result.get("nextCursor")
        print(f"  Batch {batch_idx + 1}: +{len(new_posts)} = {len(all_posts)} total")

        if not cursor:
            print("  No more pages.")
            break

        time.sleep(0.3)

    print(f"[2/5] Collection done: {len(all_posts)} posts")
    return all_posts

# ── Step: chain merging ────────────────────────────────────────────────────────

def merge_chains(posts: list[dict]) -> list[dict]:
    """
    Chain merging is now handled in JS (parsePage groups thread_items by edge).
    This function is kept only to sort by taken_at descending.
    """
    return sorted(posts, key=lambda p: p.get("taken_at", 0), reverse=True)

# ── Step: classification ───────────────────────────────────────────────────────

def keyword_score(text: str, keywords: list[str]) -> int:
    t = text.lower()
    return sum(1 for kw in keywords if kw.lower() in t)


def categorize(post: dict) -> str | None:
    """
    Initial collect step always returns None so every post is saved under
    uncategorized/. Final 10-category assignment is performed by scripts/classify.py
    via codex — the 10-category space is too fine-grained for keyword heuristics.
    """
    return None

# ── Step: save as individual markdown files ────────────────────────────────────

def make_slug(text: str) -> str:
    """Create a URL-safe slug from the first line of text (max 40 chars)."""
    first = re.split(r"[.!?\n]", text.strip())[0].strip()
    first = first[:40]
    # Keep Korean/alphanumeric; replace spaces and others with hyphens
    slug = re.sub(r"[^\w가-힣]+", "-", first, flags=re.UNICODE)
    slug = slug.strip("-").lower()
    return slug or "post"


def save_post(post: dict, username: str, category: str, output_root: Path) -> Path:
    """
    Write a single post as a markdown file.
    Path: {output_root}/{username}/{category}/{date}-{slug}.md
    Frontmatter fields: pk, username, category, taken_at, date, source, chain_pks (if present)
    """
    taken_at: int = post.get("taken_at", 0)
    dt = datetime.fromtimestamp(taken_at, tz=timezone.utc)
    date_str = dt.strftime("%Y-%m-%d")
    slug = make_slug(post["text"])

    cat_dir = output_root / username / category
    cat_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{date_str}-{slug}.md"
    filepath = cat_dir / filename

    # Build frontmatter
    fm_lines = [
        "---",
        f"pk: \"{post['pk']}\"",
        f"username: \"@{username}\"",
        f"category: \"{CATEGORY_LABELS[category]}\"",
        f"taken_at: {taken_at}",
        f"date: \"{date_str}\"",
        f"source: \"https://www.threads.net/@{username}\"",
    ]
    if post.get("chain_pks"):
        pks_yaml = "[" + ", ".join(f'"{pk}"' for pk in post["chain_pks"]) + "]"
        fm_lines.append(f"chain_pks: {pks_yaml}")
    fm_lines.append("---")

    # First line of text as H1 title
    title = re.split(r"[.!?\n]", post["text"].strip())[0].strip()
    title = title[:80] + ("..." if len(title) > 80 else "")

    content_lines = fm_lines + [
        "",
        f"# {title}",
        "",
        post["text"],
        "",
    ]

    filepath.write_text("\n".join(content_lines), encoding="utf-8")

    # Auto-label immediately after saving
    try:
        from sources.threads.label import label_file
        labels = label_file(filepath)
        if labels:
            print(f"    → 레이블: {', '.join(labels)}")
    except Exception:
        pass  # labeling is best-effort, never blocks saving

    return filepath

# ── CLI entry point ────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect Threads.net posts and save as categorized markdown files."
    )
    parser.add_argument(
        "username",
        help="Threads username, e.g. @johndoe or johndoe",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of collection batches (~50–110 posts per batch). Default: 20.",
    )
    parser.add_argument(
        "--types",
        default="",
        help="Comma-separated category slugs (13-category 체계). 비우면 전체. 예: ai-llm,monetization,viral-sns",
    )
    parser.add_argument(
        "--user-id",
        dest="user_id",
        default=None,
        help="Skip userID detection and use this numeric ID directly.",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default=None,
        help="Root output directory. Defaults to Threads/ relative to CWD.",
    )
    return parser.parse_args()


TYPE_ALIASES = {
    slug: slug for slug in CATEGORY_LABELS if slug != "uncategorized"
}


def main() -> None:
    args = parse_args()

    # Normalise username
    username = args.username.lstrip("@").strip()
    if not username:
        sys.exit("ERROR: username must not be empty.")

    # Resolve output directory
    output_root = Path(args.output_dir) if args.output_dir else Path.cwd() / "Threads"

    # Resolve requested categories (비우면 전체 13-category)
    requested_types_raw = [t.strip().lower() for t in args.types.split(",") if t.strip()]
    requested_cats: set[str] = set()
    if not requested_types_raw:
        requested_cats = set(TYPE_ALIASES.values())
    else:
        for t in requested_types_raw:
            if t in TYPE_ALIASES:
                requested_cats.add(TYPE_ALIASES[t])
            else:
                valid = ", ".join(sorted(TYPE_ALIASES.keys()))
                sys.exit(f"ERROR: Unknown type '{t}'. Valid options: {valid}.")

    print(f"ThreadCollector — @{username}")
    print(f"  Categories : {', '.join(sorted(requested_cats))}")
    print(f"  Batch limit: {args.limit}")
    print(f"  Output dir : {output_root}")
    print()

    # ── 0. Resolve browse command ────────────────────────────────────────────
    global BROWSE_CMD
    BROWSE_CMD = _resolve_browse_cmd()
    # Quick sanity: the first element must exist
    if not os.path.isfile(BROWSE_CMD[0]):
        sys.exit(
            f"ERROR: browse binary not found at:\n  {BROWSE_CMD[0]}\n"
            "Please install gstack browse first (or ensure bun is installed)."
        )

    # ── 0b. Inject Chrome session cookies (best-effort) ───────────────────────
    inject_chrome_cookies()

    # ── 1. Get userID ─────────────────────────────────────────────────────────
    user_id = args.user_id or get_user_id(username)

    # ── 2. Collect posts ──────────────────────────────────────────────────────
    raw_posts = collect_posts(username, user_id, args.limit)

    if len(raw_posts) < 10:
        print(f"WARNING: Only {len(raw_posts)} posts collected. The session may need refreshing.")

    # ── 3. Merge chains (same taken_at → same chain) ──────────────────────────
    print(f"[3/5] Merging chains ...")
    posts = merge_chains(raw_posts)
    chains_count = sum(1 for p in posts if p.get("chain_pks"))
    print(f"  {len(raw_posts)} raw posts → {len(posts)} after chain merge ({chains_count} chains)")

    # ── 4. Classify and save ──────────────────────────────────────────────────
    print(f"[4/4] Classifying and saving ...")

    stats: dict[str, int] = {cat: 0 for cat in CATEGORY_LABELS}

    for post in posts:
        cat = categorize(post)
        if cat is None:
            cat = "uncategorized"
        if cat != "uncategorized" and cat not in requested_cats:
            continue
        save_post(post, username, cat, output_root)
        stats[cat] += 1

    # ── Final report ──────────────────────────────────────────────────────────
    total_saved = sum(v for k, v in stats.items() if k != "uncategorized")
    uncat_count = stats["uncategorized"]
    print()
    print(f"ThreadCollector complete — @{username}")
    print(f"  Collected  : {len(raw_posts)} posts")
    print(f"  After merge: {len(posts)} posts ({chains_count} chains merged)")
    print(f"  Categorized: {total_saved} saved, {uncat_count} uncategorized")
    if uncat_count:
        print(f"  → Run /classify @{username} to AI-classify the uncategorized posts")
    print()
    for cat, label in CATEGORY_LABELS.items():
        if cat == "uncategorized":
            if uncat_count:
                cat_dir = output_root / username / cat
                print(f"  {cat_dir}/  ({uncat_count} files — pending /classify)")
        elif cat in requested_cats:
            cat_dir = output_root / username / cat
            print(f"  {cat_dir}/  ({stats[cat]} files)")


if __name__ == "__main__":
    main()
