#!/usr/bin/env python3
"""
ThreadCollector — generate insights/ from collected posts
Usage: python3 scripts/insights.py @username [--output-dir DIR]

Analyzes all categorized posts and writes:
  Threads/{username}/insights/overview.md
  Threads/{username}/insights/patterns.md
  Threads/{username}/insights/key-posts.md
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

CAT_DIRS = [
    "ai-llm",
    "viral-sns",
    "monetization",
    "dev-tools",
    "product-strategy",
    "startup-philosophy",
    "career-growth",
    "learning-retro",
    "productivity",
    "web-app",
]


def _find_codex() -> str | None:
    codex = shutil.which("codex")
    if codex:
        return codex
    for p in ["~/.bun/bin/codex", "~/.local/bin/codex", "/usr/local/bin/codex"]:
        expanded = os.path.expanduser(p)
        if os.path.isfile(expanded):
            return expanded
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate insights/ from collected Threads posts via codex exec."
    )
    parser.add_argument("username", help="Threads username, e.g. @kongkey__")
    parser.add_argument("--output-dir", dest="output_dir", default=None)
    args = parser.parse_args()

    username = args.username.lstrip("@").strip()
    output_root = Path(args.output_dir) if args.output_dir else Path.cwd() / "Threads"
    user_dir = output_root / username

    if not user_dir.exists():
        sys.exit(f"No data for @{username} at {user_dir}\nRun /collect first.")

    md_files = [
        f
        for cat in CAT_DIRS
        for f in (user_dir / cat).glob("*.md")
        if (user_dir / cat).exists()
    ]

    if not md_files:
        sys.exit(
            f"No categorized posts for @{username}.\n"
            "Run /collect then /classify first."
        )

    codex = _find_codex()
    if not codex:
        sys.exit("ERROR: codex not found. Install via: npm install -g @openai/codex")

    insights_dir = user_dir / "insights"
    insights_dir.mkdir(parents=True, exist_ok=True)

    cat_counts = {
        cat: len(list((user_dir / cat).glob("*.md")))
        for cat in CAT_DIRS
        if (user_dir / cat).exists()
    }
    count_summary = ", ".join(f"{cat}: {n}" for cat, n in cat_counts.items() if n)

    print(f"InsightsCollector — @{username}")
    print(f"  Posts: {len(md_files)} ({count_summary})")
    print()

    prompt = (
        f"Analyze Threads.net posts by @{username} in this directory.\n\n"
        f"Read ALL .md files in these categorized folders: {', '.join(CAT_DIRS)}. "
        f"({len(md_files)} total). Each file: YAML frontmatter + post text.\n\n"
        "Create these 3 files in insights/:\n\n"
        "**insights/overview.md**\n"
        f"Who is @{username}? What topics do they write about? What is their voice and style? "
        "Include: content breakdown by theme, key personality traits visible in the writing. "
        "(300-500 words, Korean)\n\n"
        "**insights/patterns.md**\n"
        "Recurring themes, frameworks, mental models, beliefs they push. "
        "What do they consistently advocate? Include real verbatim quotes. "
        "(400-600 words, Korean)\n\n"
        "**insights/key-posts.md**\n"
        "Curate 12-15 of the most insightful or representative posts across all categories. "
        "For each: show the original text verbatim, then a 1-2 sentence note on why it matters. "
        "Group by theme, not category. (Korean)\n\n"
        "Write all 3 files now. Do not ask for confirmation."
    )

    print(f"[1/1] Generating insights via codex ...")
    print(f"      Reading {len(md_files)} posts — this takes 60-120 seconds.")
    print()

    try:
        subprocess.run(
            [codex, "exec",
             "--full-auto", "--ephemeral",
             "--model", "gpt-5.4",
             "-s", "workspace-write",
             "-C", str(user_dir),
             prompt],
            capture_output=True, text=True, timeout=600,
        )
    except subprocess.TimeoutExpired:
        sys.exit("ERROR: codex timed out (600s). Try again or reduce post count with /collect --limit.")

    created = sorted(f.name for f in insights_dir.glob("*.md"))
    print()
    if created:
        print(f"InsightsCollector done — @{username}")
        for name in created:
            size = (insights_dir / name).stat().st_size
            print(f"  insights/{name}  ({size:,} bytes)")
    else:
        print("ERROR: insights/ files were not created.")
        sys.exit(1)


if __name__ == "__main__":
    main()
