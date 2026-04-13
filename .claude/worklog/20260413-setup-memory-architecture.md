# 2026-04-13: Memory Architecture Bootstrap

## 배경
thread-collector 프로젝트에 Claude Code 장기 메모리 구조가 전혀 없었음.
다른 프로젝트(ios-29cm, talon, wave 등)와 같은 canonical memory architecture를 이 프로젝트에도 연결하기 위해 `/setup-memory-architecture` 실행.

## 수정 내역

| 경로 | 변경 |
|------|------|
| `~/.claude/memory-arch/projects.conf` | `thread-collector=thread-collector` 추가 |
| `~/.claude/memory-arch/vaults/thread-collector/` | 신규 생성 |
| `~/.claude/memory-arch/.cache/thread-collector/` | 신규 생성 |
| `.claude/settings.json` | 신규 생성 (memory hook 2개: UserPromptSubmit, Stop) |
| `.claude/memory/.cache/` | 신규 생성 |
| `.claude/memory/scripts` | symlink → `~/.claude/memory-arch/scripts` |
| `.claude/memory/vault` | symlink → `~/.claude/memory-arch/vaults/thread-collector` |
| `~/.claude/projects/%2F.../memory/MEMORY.md` | 실파일 신규 생성 |
| `.gitignore` | memory ignore 항목 추가 |

## 검증 결과
8/8 항목 모두 OK

## 다음 단계
- 세션 종료 시마다 `/debrief` 실행해 memory 파일 갱신
- 주요 결정/피드백 발생 시 memory 파일 작성

## 핵심 교훈
memory architecture가 없으면 `/debrief`가 worklog-only fallback으로 동작.
새 프로젝트 시작 시 초반에 `/setup-memory-architecture` 실행하는 것이 좋음.
