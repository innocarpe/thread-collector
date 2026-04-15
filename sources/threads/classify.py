#!/usr/bin/env python3
"""
ThreadCollector — AI classify uncategorized posts
Usage: python3 -m sources.threads.classify @username [--output-dir DIR]

Reads Threads/{username}/uncategorized/ and classifies each post
via `codex exec`, moving files to the correct category folder.
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
}

CATEGORY_DESCRIPTIONS = {
    "ai-llm": "LLM/생성형 AI 활용, 프롬프트 엔지니어링, AI 제품/도구 리뷰, 바이브코딩",
    "viral-sns": "SNS 콘텐츠 전략, 바이럴 기법, 쇼츠·릴스·스레드 운영, 알고리즘, ASO/검색, 퍼널 마케팅",
    "monetization": "수익화 실험, 부수입, 광고수익, 가격 실험, 캐시플로우·매출 인증",
    "dev-tools": "개발 도구·에디터·CLI·스택 선택·빌드 파이프라인·워크플로우 최적화",
    "product-strategy": "제품 전략, PMF 탐색, MVP 기획, 피봇, 유저 리서치, 기능 우선순위",
    "startup-philosophy": "창업 마인드셋, 인디해킹 철학, 실패·번아웃 후기, 스타트업 인사이트",
    "career-growth": "커리어 전환, 이직·취업, 개발자·창업자 성장, 연봉·포트폴리오",
    "learning-retro": "학습법, 스킬 향상, 공부 후기, 회고, 일·프로젝트 인사이트 요약",
    "productivity": "생산성, 루틴, 타임박싱, 셀프 매니지먼트, 집중력, 업무 효율",
    "web-app": "웹/SaaS 개발, 앱 개발, 프론트/백엔드 구체 기술, 배포·인프라",
    # 신규 3개 (2026-04-15)
    "portfolio-ops": "다작·자동화·CI/CD·앱 포트폴리오 대량 운영 체계, 350앱 운영 철학, 대량출시 전략",
    "aso": "앱스토어 최적화, 키워드 리서치, 출시 체크리스트, 리뷰 대응, 플레이스토어 순위 전략",
    "case-study": "특정 앱 성공/실패 사례, 수익 인증, 리텐션 실데이터, postmortem, 실패 후기",
}

CLASSIFY_BATCH_SIZE = 20


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

    codex = find_codex()
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

        cat_lines = "\n".join(
            f'- "{slug}": {CATEGORY_DESCRIPTIONS[slug]}'
            for slug in CATEGORY_LABELS
        )
        prompt = (
            f"Read {tmp_input} — JSON array of Threads.net posts (pk + text, Korean).\n\n"
            "Classify each post into exactly ONE of these 13 categories:\n"
            f"{cat_lines}\n"
            '- "skip": junk — under 20 chars, only emojis, zero insight, pure reaction\n\n'
            "Rules:\n"
            "- Pick the single BEST fit. If a post could fit multiple, choose the one matching "
            "the post's primary topic (what the author is mainly talking about).\n"
            "- AI 도구·LLM 제품·AI 코딩 어시스턴트(Claude Code, Cursor, openclaw, Google AI Studio, "
            "Gemini, ChatGPT 등)에 대한 리뷰·사용기·소감은 무조건 'ai-llm' 으로 배정. 'dev-tools' 는 "
            "AI가 아닌 일반 개발 도구(IDE, CLI, 빌드 체인, 프레임워크, 라이브러리)에 한정.\n"
            "- AI/LLM 이야기라도 주제가 '수익화 실험'이면 monetization, '앱 만드는 기술'이면 web-app 등으로 "
            "구체 의도에 맞춰 배정할 것.\n"
            "- 'viral-sns'는 SNS 플랫폼 운영·그로스 전술에 한정. 단순 바이럴된 글 공유는 해당 주제로.\n\n"
            f"Write ONLY a JSON file to {tmp_output}:\n"
            '[{"pk": "...", "category": "..."}]\n'
            "No explanation. Only write the JSON file."
        )

        proc = None
        try:
            # Wipe any stale output from a previous batch so we can distinguish
            # "codex did not write this run" from "codex wrote a parseable file".
            if os.path.isfile(tmp_output):
                os.unlink(tmp_output)
            proc = subprocess.run(
                [codex, "exec", "--full-auto", "--ephemeral",
                 "--model", "gpt-5.4-mini",
                 "--add-dir", "/tmp",
                 prompt],
                capture_output=True, text=True, timeout=300,
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

        if classified_count:
            print(f" {classified_count} classified")
        else:
            # Surface codex stderr so rate-limit / auth / quota errors don't
            # silently turn into "everything skipped → deleted" downstream.
            print(" parse failed")
            if proc and proc.stderr:
                tail = "\n".join(proc.stderr.strip().splitlines()[-5:])
                if tail:
                    print(f"    codex stderr (tail):\n    {tail}")
            if proc and proc.stdout:
                tail = "\n".join(proc.stdout.strip().splitlines()[-5:])
                if tail and "ERROR" in tail.upper():
                    print(f"    codex stdout (tail):\n    {tail}")

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

    unresolved = 0
    for post in posts:
        cat = pk_map.get(str(post["pk"]))
        if cat == "skip":
            post["filepath"].unlink()
            skipped += 1
        elif cat in CATEGORY_LABELS:
            move_to_category(post, cat, output_root, username)
            stats[cat] += 1
        elif cat is None:
            # Codex returned no classification for this pk (rate limit, timeout,
            # parse failure, etc.). DO NOT delete — leave it in uncategorized/
            # so the next /classify run can retry.
            unresolved += 1
        else:
            failed += 1  # unknown category — leave in place

    if unresolved:
        print(
            f"  [warn] {unresolved} posts left in uncategorized/ — codex returned "
            f"no result (rate limit? timeout?). Re-run /classify to retry."
        )

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
