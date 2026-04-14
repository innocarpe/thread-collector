# 2026-04-13: ThreadCollector 인사이트 스킬 정리

## 배경
차세대 인사이트 워크플로우를 위해 /insights 스킬이 실제 `scripts/insights.py`를 실행하도록 문서화와 실행 경로를 정비하고, 사용자별로 수집된 Threads 포스트를 모두 순차적으로 분석하여 `insights/` 결과물을 자동 생성해야 했다.

## 원인 분석
- 기존 .claude/skills/insights/SKILL.md에는 스킬 메타 정보가 없어 실제 실행 단계가 누락되어 있었고, 결과적으로 쿠키나 codex가 제대로 작동했음에도 스킬 호출만으로 파일이 생성되지 않음.
- 사용자가 차례로 지정한 dalgom.bami 등 6명의 Threads 계정 전체에 대해 insights 생성이 필요했지만 스킬이 그 흐름을 주도하지 못해 수동으로 커맨드를 여러 번 실행해야 했음.

## 수정 내역
| 파일 | 주요 변경 내용 |
| --- | --- |
| `.claude/skills/insights/SKILL.md` | name/version/allowed-tools 항목을 채워 스킬이 `/insights @username`을 받을 때 실제 `python3 scripts/insights.py`를 실행하도록 정리함. |
| `CLAUDE.md` | 새 스킬을 문서화하는 섹션에 classify/insights 항목과 워크플로우 안내를 추가함. |
| `scripts/collect.py` | 상태 메시지를 5단계로 정비하고 `uncategorized` 카테고리 통계/출력을 개선함. |
| `Threads/{username}/insights/` | dalgom.bami, brxce.ai, appnomad_lab, ai_margin_, dev_shibaa, vibeceo.log 각 디렉토리에 `overview.md`, `patterns.md`, `key-posts.md`를 생성함 (codex exec 출력 성공). |

## 배포
배포 없음 (로컬 개발/스크립트 개선). 추후 PR 작성 후 다른 환경에 merge 필요.

## PR
None yet.

## 다음 단계
- 이 작업을 PR로 정리할 때 .claude/skills 변경과 새 `Threads/.../insights` 파일이 과도하게 많지 않도록 스쿼시 정책/필요한 파일만 포함 여부 판단.
- 남은 Threads 사용자에 대해서도 `/insights` 스킬 호출을 순차 진행하고, 여전히 새 사용자 추가 시 같은 흐름을 반복 확인.

## 핵심 교훈
- 스킬 정의는 단순 안내가 아니라 `name/version/allowed-tools` 같은 메타를 갖춰야 실제 실행을 자동화할 수 있으니 새 스킬 생성 시 초기부터 완전한 템플릿을 채워야 한다.
- 많은 사용자를 처리해야 할 때는 스킬 내 호출을 직접 실행하거나 wrapper 스크립트를 통해 일괄 처리하는 패턴을 미리 갖춰야 반복 명령을 줄일 수 있다.
