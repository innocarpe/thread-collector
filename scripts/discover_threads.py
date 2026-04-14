#!/usr/bin/env python3
"""
ThreadCollector — discover candidate Threads.net users to collect next.

Phase 1: Corpus mention mining.
Scans the existing Threads/ corpus for @username mentions that point to
users we haven't collected yet, ranks them by frequency + topic overlap
with the user's interests, and writes a markdown report to
.claude/discover-threads/YYYYMMDD-candidates.md so the user can skim the
candidates in their browser and decide who to /collect next.

Usage:
    python3 scripts/discover_threads.py
    python3 scripts/discover_threads.py --interest ai-llm,monetization
    python3 scripts/discover_threads.py --limit 15 --min-mentions 2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

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


@dataclass
class Candidate:
    handle: str
    mentions: int = 0
    category_counts: Counter = field(default_factory=Counter)
    source_users: set = field(default_factory=set)
    contexts: list = field(default_factory=list)  # list of (src_user, snippet)
    score: float = 0.0


# ── Interest resolution ───────────────────────────────────────────────────────

def load_interests_from_file() -> list[str] | None:
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


def derive_interests_from_corpus() -> list[tuple[str, int]]:
    """Top categories in the existing corpus, (slug, count) pairs."""
    counts = Counter()
    for user_dir in THREADS_ROOT.iterdir():
        if not user_dir.is_dir():
            continue
        for cat in CATEGORY_SLUGS:
            cdir = user_dir / cat
            if cdir.is_dir():
                counts[cat] += sum(1 for _ in cdir.glob("*.md"))
    return counts.most_common()


def resolve_interests(cli_arg: str | None) -> tuple[list[str], str]:
    """
    Returns (interest_slugs, source_label).
    Priority: CLI arg > .thread-collector-interests.json > auto-derived top 3.
    """
    if cli_arg:
        slugs = [s.strip() for s in cli_arg.split(",") if s.strip()]
        return slugs, f"CLI --interest"

    from_file = load_interests_from_file()
    if from_file:
        return from_file, f"{INTEREST_FILE}"

    top = derive_interests_from_corpus()[:3]
    return [slug for slug, _ in top], "auto-derived from corpus (top 3)"


# ── Corpus scanning ───────────────────────────────────────────────────────────

def existing_user_handles() -> set[str]:
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
    """Return a short snippet around the match position."""
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
    """Reject handles that look like version numbers, timestamps, or code fragments."""
    if not handle or len(handle) < 2 or len(handle) > 30:
        return False
    # Must contain at least one letter (a-z). Pure digits/dots/underscores
    # are almost always matches on version numbers like "1.0.88".
    if not re.search(r"[a-z]", handle):
        return False
    return True


def mine_corpus(existing: set[str]) -> dict[str, Candidate]:
    candidates: dict[str, Candidate] = {}
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

def score_candidates(candidates: dict[str, Candidate], interests: list[str]) -> None:
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
    candidates: list[Candidate],
    interests: list[str],
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
