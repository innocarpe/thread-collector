#!/usr/bin/env python3
"""
ThreadCollector — AI classify uncategorized posts
Usage: python3 scripts/classify.py @username [--output-dir DIR]

Reads Threads/{username}/uncategorized/ and classifies each post
via `codex exec`, moving files to the correct category folder.
Junk posts are deleted.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CATEGORY_LABELS = {
    "tech-dev": "기술/개발",
    "product-business": "프로덕트/비즈니스",
    "career-philosophy": "커리어/철학",
}

CLASSIFY_BATCH_SIZE = 60


def _find_codex() -> str | None:
    codex = shutil.which("codex")
    if codex:
        return codex
    for p in ["~/.bun/bin/codex", "~/.local/bin/codex", "/usr/local/bin/codex"]:
        expanded = os.path.expanduser(p)
        if os.path.isfile(expanded):
            return expanded
    return None


def parse_md_post(filepath: Path) -> dict | None:
    """Extract pk and text from a ThreadCollector markdown file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    fm_text = parts[1]
    body = parts[2].strip()

    pk_match = re.search(r'^pk:\s*["\']?(\d+)["\']?', fm_text, re.MULTILINE)
    if not pk_match:
        return None

    # Skip H1 title line, rest is post text
    lines = body.split("\n")
    text_lines = []
    found_title = False
    for line in lines:
        if not found_title and line.startswith("#"):
            found_title = True
            continue
        if found_title:
            text_lines.append(line)

    text = "\n".join(text_lines).strip() or body

    return {
        "pk": pk_match.group(1),
        "text": text,
        "filepath": filepath,
        "content": content,
        "frontmatter": fm_text,
    }


def codex_classify(posts: list[dict]) -> dict[str, str]:
    """
    Classify posts via codex exec.
    Returns {pk: category} where category ∈ CATEGORY_LABELS keys | "skip".
    """
    if not posts:
        return {}

    codex = _find_codex()
    if not codex:
        print("[warn] codex not found — cannot AI-classify")
        return {}

    result: dict[str, str] = {}
    total_batches = (len(posts) + CLASSIFY_BATCH_SIZE - 1) // CLASSIFY_BATCH_SIZE

    for batch_idx in range(total_batches):
        batch = posts[batch_idx * CLASSIFY_BATCH_SIZE : (batch_idx + 1) * CLASSIFY_BATCH_SIZE]
        batch_num = batch_idx + 1
        print(f"  Batch {batch_num}/{total_batches}: {len(batch)} posts ...", end="", flush=True)

        tmp_input = f"/tmp/tc_classify_in_{batch_idx}.json"
        tmp_output = f"/tmp/tc_classify_out_{batch_idx}.json"

        with open(tmp_input, "w", encoding="utf-8") as f:
            json.dump(
                [{"pk": p["pk"], "text": p["text"][:300]} for p in batch],
                f, ensure_ascii=False,
            )

        prompt = (
            f"Read {tmp_input} — JSON array of Threads.net posts (pk + text, Korean).\n\n"
            "Classify each post into exactly one category:\n"
            '- "tech-dev": coding, AI/LLM, dev tools, app development, architecture\n'
            '- "product-business": monetization, SaaS, indie hacking, marketing, '
            "viral/SNS tactics, growth, startup, PMF\n"
            '- "career-philosophy": mindset, retrospectives, learning, productivity, '
            "life philosophy\n"
            '- "skip": junk — under 20 chars, only emojis, zero insight, pure reaction\n\n'
            f"Write ONLY a JSON file to {tmp_output}:\n"
            '[{"pk": "...", "category": "..."}]\n'
            "No explanation. Only write the JSON file."
        )

        try:
            subprocess.run(
                [codex, "exec", "--full-auto", "--ephemeral",
                 "--model", "gpt-5.4-mini",
                 "--add-dir", "/tmp",
                 prompt],
                capture_output=True, text=True, timeout=180,
            )
        except subprocess.TimeoutExpired:
            print(" timeout")
            continue

        classified_count = 0
        if os.path.isfile(tmp_output):
            try:
                raw = open(tmp_output, encoding="utf-8").read().strip()
                m = re.search(r"\[.*?\]", raw, re.DOTALL)
                if m:
                    items = json.loads(m.group())
                    for item in items:
                        if "pk" in item and "category" in item:
                            result[str(item["pk"])] = item["category"]
                    classified_count = sum(1 for p in batch if str(p["pk"]) in result)
            except Exception:
                pass

        print(f" {classified_count} classified" if classified_count else " parse failed")

    return result


def move_to_category(post_data: dict, category: str, output_root: Path, username: str) -> None:
    """Move file from uncategorized/ to target category, updating frontmatter."""
    new_label = CATEGORY_LABELS[category]
    new_fm = re.sub(
        r'^(category:\s*)"[^"]*"',
        f'\\1"{new_label}"',
        post_data["frontmatter"],
        flags=re.MULTILINE,
    )
    new_content = post_data["content"].replace(post_data["frontmatter"], new_fm, 1)

    target_dir = output_root / username / category
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / post_data["filepath"].name
    target_path.write_text(new_content, encoding="utf-8")
    post_data["filepath"].unlink()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI-classify uncategorized Threads posts via codex exec."
    )
    parser.add_argument("username", help="Threads username, e.g. @kongkey__")
    parser.add_argument("--output-dir", dest="output_dir", default=None)
    args = parser.parse_args()

    username = args.username.lstrip("@").strip()
    output_root = Path(args.output_dir) if args.output_dir else Path.cwd() / "Threads"
    uncat_dir = output_root / username / "uncategorized"

    if not uncat_dir.exists():
        sys.exit(
            f"No uncategorized/ folder at {uncat_dir}\n"
            "Run /collect first, or there may be nothing to classify."
        )

    md_files = sorted(uncat_dir.glob("*.md"))
    if not md_files:
        print(f"No uncategorized posts for @{username} — already clean!")
        sys.exit(0)

    print(f"ClassifyCollector — @{username}")
    print(f"  Found {len(md_files)} uncategorized posts")
    print()

    posts = [d for f in md_files if (d := parse_md_post(f)) is not None]
    print(f"[1/2] Parsed {len(posts)} posts, sending to codex ...")
    pk_map = codex_classify(posts)

    print(f"\n[2/2] Applying classifications ...")
    stats = {cat: 0 for cat in CATEGORY_LABELS}
    skipped = 0
    failed = 0

    for post in posts:
        cat = pk_map.get(str(post["pk"]))
        if not cat or cat == "skip":
            post["filepath"].unlink()
            skipped += 1
        elif cat in CATEGORY_LABELS:
            move_to_category(post, cat, output_root, username)
            stats[cat] += 1
        else:
            failed += 1  # unknown category — leave in place

    # Remove uncategorized dir if now empty
    try:
        uncat_dir.rmdir()
    except OSError:
        remaining = len(list(uncat_dir.glob("*.md")))
        if remaining:
            print(f"  {remaining} posts left unclassified in uncategorized/")

    print()
    print(f"ClassifyCollector done — @{username}")
    for cat in CATEGORY_LABELS:
        if stats[cat]:
            print(f"  → {cat}/  +{stats[cat]}")
    print(f"  Skipped (junk/irrelevant): {skipped}")
    if failed:
        print(f"  Failed (unknown category): {failed}")


if __name__ == "__main__":
    main()
