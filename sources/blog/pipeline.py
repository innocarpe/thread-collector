"""블로그 수집 파이프라인 CLI entry point.

discover + fetch + store 오케스트레이션.

사용법:
    python3 -m sources.blog.pipeline --slug programmingzombie --dry-run --limit 10
    python3 -m sources.blog.pipeline --all-priority 1
"""
from __future__ import annotations

import argparse
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

# repo 루트를 sys.path에 추가 (다른 sources/ 모듈 import 허용)
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import yaml  # PyYAML — 이미 설치됨 (CLAUDE.md 확인)

from sources.blog.adapters import get_adapter
from sources.blog.collect import PostRef
from sources.blog.store import already_collected, save_post

logger = logging.getLogger(__name__)

_TARGETS_YAML = Path(__file__).parent / "targets.yaml"
_LOGS_DIR = Path(__file__).parent / "logs"


# ─────────────────────────────────────────────────────────
# 로깅 설정
# ─────────────────────────────────────────────────────────

def _setup_logging(slug: str) -> logging.Logger:
    """slug별 로그 파일 + stderr 핸들러를 설정한다."""
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = _LOGS_DIR / f"{slug}-{date_str}.log"

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # 파일 핸들러
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    fh.setLevel(logging.DEBUG)

    # stderr 핸들러 (INFO 이상)
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    sh.setLevel(logging.INFO)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(fh)
    root.addHandler(sh)

    return logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# targets.yaml 로드
# ─────────────────────────────────────────────────────────

def _load_targets() -> list[dict]:
    """targets.yaml에서 creator 목록을 로드한다."""
    with open(_TARGETS_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("creators", [])


def _get_creator(slug: str) -> dict | None:
    """slug로 creator 설정을 반환한다."""
    for creator in _load_targets():
        if creator.get("slug") == slug:
            return creator
    return None


def _get_creators_by_priority(max_priority: int) -> list[dict]:
    """priority <= max_priority인 creator 목록을 반환한다."""
    return [c for c in _load_targets() if c.get("priority", 99) <= max_priority]


# ─────────────────────────────────────────────────────────
# 수집 실행
# ─────────────────────────────────────────────────────────

def run_creator(
    creator: dict,
    limit: int | None,
    output_dir: Path,
    dry_run: bool,
    force: bool,
) -> dict:
    """단일 creator의 글을 수집한다.

    Returns:
        수집 결과 통계 dict
    """
    slug = creator["slug"]
    urls: list[str] = creator.get("urls", [])
    adapter_hint: str = creator.get("adapter", "auto")
    rate_limit: float = float(creator.get("rate_limit_sec", 2.0))

    log = logging.getLogger(f"pipeline.{slug}")
    log.info("=== %s 수집 시작 (adapter=%s) ===", slug, adapter_hint)

    stats = {
        "slug": slug,
        "discovered": 0,
        "fetched": 0,
        "saved": 0,
        "skipped_dedup": 0,
        "failed": 0,
    }

    for root_url in urls:
        log.info("discover_posts: %s", root_url)
        adapter = get_adapter(root_url, hint=adapter_hint)

        # discover
        try:
            posts: list[PostRef] = adapter.discover_posts(root_url)
        except Exception as exc:
            log.error("discover 실패: %s — %s", root_url, exc)
            stats["failed"] += 1
            continue

        if limit:
            posts = posts[:limit]

        stats["discovered"] += len(posts)
        log.info("%s: %d개 포스트 발견", root_url, len(posts))

        if dry_run:
            log.info("[dry-run] 저장 스킵. 샘플 3개:")
            for ref in posts[:3]:
                log.info("  - %s | %s | %s", ref.url, ref.title, ref.published_at)
            continue

        # fetch + store
        for i, ref in enumerate(posts):
            canonical = ref.canonical_url or ref.url

            # dedup 확인
            if not force and already_collected(slug, canonical, output_dir):
                log.debug("dedup skip: %s", canonical)
                stats["skipped_dedup"] += 1
                continue

            # rate limit
            if i > 0:
                time.sleep(rate_limit)

            try:
                post = adapter.fetch_post(ref)
                stats["fetched"] += 1
            except Exception as exc:
                log.warning("fetch 실패: %s — %s", ref.url, exc)
                stats["failed"] += 1
                continue

            try:
                saved_path = save_post(
                    creator_slug=slug,
                    post=post,
                    category="uncategorized",
                    output_root=output_dir,
                )
                stats["saved"] += 1
                log.debug("저장: %s", saved_path)
            except Exception as exc:
                log.warning("저장 실패: %s — %s", ref.url, exc)
                stats["failed"] += 1

    log.info(
        "=== %s 완료: discovered=%d, saved=%d, skipped=%d, failed=%d ===",
        slug,
        stats["discovered"],
        stats["saved"],
        stats["skipped_dedup"],
        stats["failed"],
    )
    return stats


# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m sources.blog.pipeline",
        description="블로그 수집 파이프라인 (discover → fetch → store)",
    )
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument(
        "--slug",
        metavar="SLUG",
        help="수집할 creator slug (targets.yaml 기준)",
    )
    target_group.add_argument(
        "--all-priority",
        type=int,
        metavar="N",
        dest="all_priority",
        help="priority N 이하인 모든 creator 수집",
    )
    parser.add_argument(
        "--limit",
        type=int,
        metavar="N",
        default=None,
        help="creator당 최대 수집 글 수",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("Blog"),
        metavar="PATH",
        dest="output_dir",
        help="저장 루트 디렉토리 (기본: Blog/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="discover만 하고 저장하지 않음",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="dedup 무시하고 재수집",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    # 수집 대상 creator 목록 결정
    if args.slug:
        creator = _get_creator(args.slug)
        if creator is None:
            print(f"ERROR: slug '{args.slug}'를 targets.yaml에서 찾을 수 없습니다.", file=sys.stderr)
            return 1
        creators = [creator]
    else:
        creators = _get_creators_by_priority(args.all_priority)
        if not creators:
            print(f"ERROR: priority {args.all_priority} 이하인 creator가 없습니다.", file=sys.stderr)
            return 1

    # 첫 번째 slug로 로그 설정 (다중 creator면 "batch")
    log_slug = creators[0]["slug"] if len(creators) == 1 else "batch"
    _setup_logging(log_slug)

    all_stats: list[dict] = []
    for creator in creators:
        stats = run_creator(
            creator=creator,
            limit=args.limit,
            output_dir=args.output_dir,
            dry_run=args.dry_run,
            force=args.force,
        )
        all_stats.append(stats)

    # 요약 출력
    print("\n── 수집 요약 ──", file=sys.stderr)
    for s in all_stats:
        print(
            f"  {s['slug']}: discovered={s['discovered']}, saved={s['saved']}, "
            f"skipped={s['skipped_dedup']}, failed={s['failed']}",
            file=sys.stderr,
        )

    total_failed = sum(s["failed"] for s in all_stats)
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
