#!/usr/bin/env python3
"""
NaverCafe — AI classify uncategorized community posts
Usage: python3 -m sources.naver_cafe.classify vibemoney

Reads NaverCafe/{cafe}/community/uncategorized/ and classifies each post
via codex exec, moving files to the correct category folder.
Junk posts are deleted.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# repo 루트를 sys.path에 추가 (직접 실행 및 -m 호출 모두 지원)
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sources._common.codex import find_codex

CATEGORY_LABELS = {
    "income-methods": "수익화 방법",
    "tools-ai":       "도구/AI/자동화",
    "case-studies":   "성공 사례/후기",
    "marketing":      "마케팅/콘텐츠",
}

CLASSIFY_BATCH_SIZE = 50


def parse_md_post(filepath: Path) -> dict | None:
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

    article_id_match = re.search(r"^article_id:\s*(\d+)", fm_text, re.MULTILINE)
    if not article_id_match:
        return None

    # 제목 + 본문 합쳐서 분류 텍스트로 사용
    lines = body.split("\n")
    text_lines = []
    found_title = False
    for line in lines:
        if not found_title and line.startswith("#"):
            found_title = True
            text_lines.append(line.lstrip("#").strip())
            continue
        if found_title:
            text_lines.append(line)
    text = "\n".join(text_lines).strip() or body

    return {
        "id": article_id_match.group(1),
        "text": text,
        "filepath": filepath,
        "content": content,
        "frontmatter": fm_text,
    }


def codex_classify(posts: list[dict]) -> dict[str, str]:
    """Classify posts via codex exec. Returns {article_id: category}."""
    if not posts:
        return {}

    codex = find_codex()
    if not codex:
        print("[warn] codex not found — cannot AI-classify")
        return {}

    result: dict[str, str] = {}
    total_batches = (len(posts) + CLASSIFY_BATCH_SIZE - 1) // CLASSIFY_BATCH_SIZE

    for batch_idx in range(total_batches):
        batch = posts[batch_idx * CLASSIFY_BATCH_SIZE:(batch_idx + 1) * CLASSIFY_BATCH_SIZE]
        batch_num = batch_idx + 1
        print(f"  Batch {batch_num}/{total_batches}: {len(batch)}개 ...", end="", flush=True)

        tmp_input  = f"/tmp/nc_classify_in_{batch_idx}.json"
        tmp_output = f"/tmp/nc_classify_out_{batch_idx}.json"

        with open(tmp_input, "w", encoding="utf-8") as f:
            json.dump(
                [{"id": p["id"], "text": p["text"][:400]} for p in batch],
                f, ensure_ascii=False,
            )

        prompt = (
            f"Read {tmp_input} — JSON array of Naver Cafe posts (id + text, Korean).\n\n"
            "This cafe is about AI-based vibe coding and online monetization (바이브코딩, 온라인 수익화).\n\n"
            "Classify each post into exactly one category:\n"
            '- "income-methods": how to make money — freelance, gig work, payment systems, '
            "digital products, affiliate, adsense, platform sales, revenue strategies\n"
            '- "tools-ai": AI tools, coding tools, automation — Claude, GPT, Gemini, '
            "Cursor, Anti-Gravity, OpenClaw, Netlify, n8n, Make.com, no-code/low-code\n"
            '- "case-studies": actual results/reviews — success stories, failure stories, '
            "course reviews, earnings proof, project launches\n"
            '- "marketing": SNS marketing, content strategy, traffic, SEO, '
            "newsletters, funnels, personal branding\n"
            '- "skip": junk — pure greetings, under 30 chars, no useful info, '
            "generic questions with no context\n\n"
            f"Write ONLY a JSON file to {tmp_output}:\n"
            '[{"id": "...", "category": "..."}]\n'
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
                        if "id" in item and "category" in item:
                            result[str(item["id"])] = item["category"]
                    classified_count = sum(1 for p in batch if str(p["id"]) in result)
            except Exception:
                pass

        print(f" {classified_count}개 분류됨" if classified_count else " 파싱 실패")

    return result


def move_to_category(post_data: dict, category: str,
                     community_dir: Path) -> None:
    """uncategorized/ → 대상 카테고리 폴더로 이동, frontmatter category 업데이트."""
    new_label = CATEGORY_LABELS[category]
    new_fm = re.sub(
        r'^(category:\s*)"[^"]*"',
        f'\\1"{new_label}"',
        post_data["frontmatter"],
        flags=re.MULTILINE,
    )
    new_content = post_data["content"].replace(post_data["frontmatter"], new_fm, 1)

    target_dir = community_dir / category
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / post_data["filepath"].name
    target_path.write_text(new_content, encoding="utf-8")
    post_data["filepath"].unlink()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="NaverCafe AI Classifier — uncategorized → category"
    )
    parser.add_argument("cafe_name", help="카페 슬러그 (예: vibemoney)")
    parser.add_argument("--output-dir", dest="output_dir", default=None)
    args = parser.parse_args()

    cafe_name  = args.cafe_name.strip().lower()
    output_root = Path(args.output_dir) if args.output_dir else Path.cwd() / "NaverCafe"
    community_dir = output_root / cafe_name / "community"
    uncat_dir = community_dir / "uncategorized"

    if not uncat_dir.exists():
        sys.exit(
            f"uncategorized/ 폴더 없음: {uncat_dir}\n"
            "python3 scripts/collect_naver.py {cafe_name} 를 먼저 실행하세요."
        )

    md_files = sorted(uncat_dir.glob("*.md"))
    if not md_files:
        print(f"{cafe_name} uncategorized 글 없음 — 이미 깨끗합니다!")
        sys.exit(0)

    print(f"NaverCafe Classifier — {cafe_name}")
    print(f"  미분류: {len(md_files)}개")
    print()

    posts = [d for f in md_files if (d := parse_md_post(f)) is not None]
    print(f"[1/2] {len(posts)}개 파싱 완료, codex 전송 중 ...")
    id_map = codex_classify(posts)

    print(f"\n[2/2] 분류 적용 중 ...")
    stats = {cat: 0 for cat in CATEGORY_LABELS}
    skipped = 0
    failed  = 0

    for post in posts:
        cat = id_map.get(str(post["id"]))
        if not cat or cat == "skip":
            post["filepath"].unlink()
            skipped += 1
        elif cat in CATEGORY_LABELS:
            move_to_category(post, cat, community_dir)
            stats[cat] += 1
        else:
            failed += 1  # 알 수 없는 카테고리 — 그대로 둠

    try:
        uncat_dir.rmdir()
    except OSError:
        remaining = len(list(uncat_dir.glob("*.md")))
        if remaining:
            print(f"  {remaining}개 미분류 상태로 남음")

    print()
    print(f"NaverCafe Classifier 완료 — {cafe_name}")
    for cat, label in CATEGORY_LABELS.items():
        if stats[cat]:
            print(f"  → {cat}/  +{stats[cat]}")
    print(f"  삭제(junk): {skipped}")
    if failed:
        print(f"  실패(알 수 없는 카테고리): {failed}")


if __name__ == "__main__":
    main()
