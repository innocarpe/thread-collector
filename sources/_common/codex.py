#!/usr/bin/env python3
"""codex CLI 경로 탐색 공통 유틸.

4개 파일(threads/classify.py, naver_cafe/classify.py,
threads/insights.py, naver_cafe/insights.py)에 복붙됐던
_find_codex() 함수를 단일 출처로 통합.
"""
from __future__ import annotations

import os
import shutil


def find_codex() -> str | None:
    """codex 실행 파일 경로를 반환. PATH → ~/.bun/bin → ~/.local/bin → /usr/local/bin 순."""
    codex = shutil.which("codex")
    if codex:
        return codex
    for p in ["~/.bun/bin/codex", "~/.local/bin/codex", "/usr/local/bin/codex"]:
        expanded = os.path.expanduser(p)
        if os.path.isfile(expanded):
            return expanded
    return None
