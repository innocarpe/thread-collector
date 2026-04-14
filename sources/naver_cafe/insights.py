#!/usr/bin/env python3
"""
NaverCafe — generate insights/ from collected posts
Usage: python3 scripts/insights_naver.py vibemoney

Analyzes operator + community posts and writes:
  NaverCafe/{cafe}/insights/operator/full-analysis.md
  NaverCafe/{cafe}/insights/operator/income-methods.md
  NaverCafe/{cafe}/insights/operator/tools-stack.md
  NaverCafe/{cafe}/insights/operator/marketing-tactics.md
  NaverCafe/{cafe}/insights/community/income-methods.md
  NaverCafe/{cafe}/insights/community/tools-ai.md
  NaverCafe/{cafe}/insights/community/case-studies.md
  NaverCafe/{cafe}/insights/community/qa-pain-points.md
  NaverCafe/{cafe}/insights/00-overview.md
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

OPERATOR_CATS  = ["income-methods", "tools-ai", "case-studies", "marketing"]
COMMUNITY_CATS = ["income-methods", "tools-ai", "case-studies", "marketing", "uncategorized"]


def _find_codex() -> str | None:
    codex = shutil.which("codex")
    if codex:
        return codex
    for p in ["~/.bun/bin/codex", "~/.local/bin/codex", "/usr/local/bin/codex"]:
        expanded = os.path.expanduser(p)
        if os.path.isfile(expanded):
            return expanded
    return None


def count_posts(base_dir: Path, cats: list[str]) -> dict[str, int]:
    return {
        cat: len(list((base_dir / cat).glob("*.md")))
        for cat in cats
        if (base_dir / cat).exists()
    }


def run_codex(codex: str, work_dir: Path, prompt: str, label: str) -> bool:
    print(f"  [{label}] codex 실행 중 ...", flush=True)
    try:
        subprocess.run(
            [codex, "exec", "--full-auto", "--ephemeral",
             "--model", "gpt-5.4",
             "-s", "workspace-write",
             "-C", str(work_dir),
             prompt],
            capture_output=True, text=True, timeout=600,
        )
        return True
    except subprocess.TimeoutExpired:
        print(f"  [{label}] timeout (600s)")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="NaverCafe 인사이트 생성기"
    )
    parser.add_argument("cafe_name", help="카페 슬러그 (예: vibemoney)")
    parser.add_argument("--output-dir", dest="output_dir", default=None)
    parser.add_argument(
        "--only",
        choices=["operator", "community", "overview"],
        default=None,
        help="특정 섹션만 생성",
    )
    args = parser.parse_args()

    cafe_name   = args.cafe_name.strip().lower()
    output_root = Path(args.output_dir) if args.output_dir else Path.cwd() / "NaverCafe"
    cafe_dir    = output_root / cafe_name

    if not cafe_dir.exists():
        sys.exit(f"카페 데이터 없음: {cafe_dir}\npython3 scripts/collect_naver.py {cafe_name} 를 먼저 실행하세요.")

    codex = _find_codex()
    if not codex:
        sys.exit("ERROR: codex not found. npm install -g @openai/codex 로 설치하세요.")

    op_dir   = cafe_dir / "operator"
    cm_dir   = cafe_dir / "community"
    ins_dir  = cafe_dir / "insights"
    ins_dir.mkdir(parents=True, exist_ok=True)
    (ins_dir / "operator").mkdir(exist_ok=True)
    (ins_dir / "community").mkdir(exist_ok=True)

    op_counts = count_posts(op_dir, OPERATOR_CATS)
    cm_counts = count_posts(cm_dir, COMMUNITY_CATS)
    op_total  = sum(op_counts.values())
    cm_total  = sum(cm_counts.values())

    print(f"NaverCafe InsightsCollector — {cafe_name}")
    print(f"  운영자: {op_total}개  ({', '.join(f'{c}:{n}' for c,n in op_counts.items() if n)})")
    print(f"  커뮤니티: {cm_total}개  ({', '.join(f'{c}:{n}' for c,n in cm_counts.items() if n)})")
    print()

    # ── 1. 운영자 인사이트 ───────────────────────────────────────────────────
    if args.only in (None, "operator") and op_total > 0:
        print("[1/3] 운영자 인사이트 생성 ...")

        op_prompt = (
            f"이 디렉토리는 네이버 카페 '{cafe_name}'의 운영자(관리자) 글 모음입니다.\n"
            f"operator/ 하위 카테고리 폴더({', '.join(OPERATOR_CATS)})의 .md 파일을 모두 읽으세요.\n"
            f"각 파일은 YAML frontmatter + 본문으로 구성됩니다.\n\n"
            "다음 4개 파일을 insights/operator/ 에 작성하세요:\n\n"
            "**insights/operator/full-analysis.md**\n"
            "운영자 글 전수 분석. 포함 내용:\n"
            "1. 글 전체 목록 테이블 (날짜, 제목, 게시판, 핵심 주장 한 줄)\n"
            "2. 정보 가치 평가 — 글마다 '실행 가능 / 홍보성 / 혼합' 구분\n"
            "3. 강의/상품 판매 구조 및 타임라인 (있다면)\n"
            "4. 수익 인증 분석 — 어떤 증거가 있고 신뢰도는?\n"
            "5. 진위 판단 — 과장/사기 여부 솔직하게\n"
            "6. 독자 관점에서 실제 얻을 수 있는 가치\n\n"
            "**insights/operator/income-methods.md**\n"
            "운영자가 언급한 수익화 방법 정리. 방법별로:\n"
            "방법명 / 설명 / 실행 단계 / 예상 수익(언급 시) / 현실성 평가\n\n"
            "**insights/operator/tools-stack.md**\n"
            "운영자가 사용/추천한 기술 스택. 카테고리별(AI 코딩툴, 호스팅, DB, 결제, 외주 플랫폼, 자동화 등)로 정리.\n"
            "각 툴: 언급 맥락 / 무료 여부 / 난이도\n\n"
            "**insights/operator/marketing-tactics.md**\n"
            "운영자의 마케팅 전술 분석:\n"
            "1. 콘텐츠 → 판매 퍼널 구조\n"
            "2. 후킹 전술 목록 (구체적 인용 포함)\n"
            "3. 신뢰 구축 방법\n"
            "4. SNS 트래픽 → 카페 → 강의 연결 구조\n"
            "5. 참고할 부분 / 피해야 할 부분\n\n"
            "한국어로 작성. 마크다운 형식. 구체적 수치/인용 포함. 미사여구 없이."
        )
        run_codex(codex, cafe_dir, op_prompt, "운영자")

    # ── 2. 커뮤니티 인사이트 ─────────────────────────────────────────────────
    if args.only in (None, "community") and cm_total > 0:
        print("[2/3] 커뮤니티 인사이트 생성 ...")

        cm_prompt = (
            f"이 디렉토리는 네이버 카페 '{cafe_name}'의 커뮤니티(일반 회원) 글 모음입니다.\n"
            f"community/ 하위 카테고리 폴더({', '.join(COMMUNITY_CATS)})의 .md 파일에서\n"
            "각 폴더별로 최신 50개 + 오래된 30개를 샘플링해서 읽으세요.\n\n"
            "다음 4개 파일을 insights/community/ 에 작성하세요:\n\n"
            "**insights/community/income-methods.md**\n"
            "커뮤니티가 실제로 시도하는 수익화 방법:\n"
            "1. 방법별 언급 빈도 테이블\n"
            "2. 구체적 성공 사례 (수치/출처 포함)\n"
            "3. 막히는 지점들 — '안 된다' 패턴\n"
            "4. 수익화 단계별 분포 (시작전/시도중/수익냄)\n\n"
            "**insights/community/tools-ai.md**\n"
            "AI 도구 사용 패턴:\n"
            "1. 도구별 언급 빈도\n"
            "2. 자주 쓰이는 도구 조합\n"
            "3. 비용/불만 관련 언급\n"
            "4. 커뮤니티 표준 스택\n\n"
            "**insights/community/case-studies.md**\n"
            "성공/실패 사례 정리:\n"
            "1. 성공 사례 목록 (수익/성과/방법/출처)\n"
            "2. 실패/포기 사례\n"
            "3. 공통점 분석\n"
            "4. 주목할 만한 사례 상세 기술\n\n"
            "**insights/community/qa-pain-points.md**\n"
            "반복되는 질문과 고민:\n"
            "1. 자주 묻는 질문 TOP 20\n"
            "2. 단계별 막힘 포인트 (환경설정→첫앱→배포→수익화)\n"
            "3. 심리적 불안 패턴\n"
            "4. 해결 안 된 채 방치되는 질문들\n\n"
            "한국어. 마크다운. 구체적 인용과 article_id 출처 포함. 미사여구 없이."
        )
        run_codex(codex, cafe_dir, cm_prompt, "커뮤니티")

    # ── 3. 전체 overview ─────────────────────────────────────────────────────
    if args.only in (None, "overview"):
        print("[3/3] overview 생성 ...")

        ov_prompt = (
            f"이 디렉토리는 네이버 카페 '{cafe_name}' 분석 결과입니다.\n"
            "insights/operator/ 와 insights/community/ 의 모든 .md 파일을 읽고\n"
            "insights/00-overview.md 를 작성하세요.\n\n"
            "포함 내용:\n"
            "1. 카페 개요 — 성격, 운영자, 콘텐츠 규모\n"
            "2. 파일 구조 안내 — 무엇을 보려면 어디로 가야 하는지\n"
            "3. 핵심 발견 Top 10\n"
            "4. 이 카페에서 보이는 시장 구조 (국내 바이브코딩/수익화 생태계 현황)\n"
            "5. 운영자 요약 판단 — 신뢰도, 강의 가치\n"
            "6. 커뮤니티 3대 공통 문제\n"
            "7. 독자 사업에 시사하는 기회\n"
            "8. 추가 수집 권장 사항\n\n"
            "한국어. 마크다운. 각 섹션에서 하위 파일 링크 포함. 군더더기 없이."
        )
        run_codex(codex, cafe_dir, ov_prompt, "overview")

    # ── 결과 확인 ─────────────────────────────────────────────────────────────
    created = sorted(ins_dir.rglob("*.md"))
    print()
    if created:
        print(f"InsightsCollector 완료 — {cafe_name}")
        for f in created:
            rel = f.relative_to(ins_dir)
            size = f.stat().st_size
            print(f"  insights/{rel}  ({size:,} bytes)")
    else:
        print("ERROR: insights/ 파일이 생성되지 않았습니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()
