---
description: 전체 변경사항을 atomic 단위로 커밋한다. 한글 Conventional Commit과 scope 규칙을 지키며 주제별로 분리한다. Examples: '커밋해줘', '변경 저장', 'commit changes'.
argument-hint: "[없음]"
---

# 전체 변경사항 커밋

## 절차

1. `git status`, `git diff --cached --stat`, `git diff --stat`, `git log --oneline -5`로 상태를 확인한다.
2. 변경을 논리 단위로 나눌 수 있는지 판단한다.
3. 여러 주제가 섞여 있으면 atomic 기준으로 분리한다.
4. 각 커밋 메시지를 한글 Conventional Commit 형식으로 작성한다.
5. HEREDOC 방식으로 커밋한다.

## 규칙

- 하나의 커밋에 하나의 논리적 변경만 담는다.
- `git commit -a`, `git commit --all`은 사용하지 않는다.
- HEREDOC 방식과 Co-Authored-By를 유지한다.
- API 키, 쿠키, 액세스 토큰 등 민감정보 포함 여부를 먼저 점검한다.

## Scope 예시

| scope | 대상 |
|-------|------|
| `collect` | 수집 스크립트, GraphQL, browse 로직 |
| `skills` | `.claude/skills/` 스킬 파일 |
| `blog` | 블로그 UI, 컴포넌트, API |
| `config` | 설정 파일, `.claude/settings.json` |
| `docs` | README, CLAUDE.md, worklog |

## 검증 체크리스트

- [ ] 하나의 커밋에 하나의 주제만 담았는가
- [ ] scope가 적절한가
- [ ] 한국어 Conventional Commit 형식인가
- [ ] Co-Authored-By가 포함됐는가
- [ ] 민감정보(API 키, 쿠키, 토큰)가 없는가
