---
description: staged area에 있는 변경만 커밋한다. unstaged 변경은 건드리지 않고 staged 상태만 기준으로 저장한다. Examples: 'staged만 커밋', '선택한 파일만 커밋'.
argument-hint: "[없음]"
---

# Staged 변경만 커밋

## 절차

1. `git diff --cached --stat`, `git status`, `git log --oneline -5`로 staged 상태를 확인한다.
2. staged area가 비어 있으면 중단한다.
3. staged 변경만 기준으로 커밋 메시지를 만든다.
4. HEREDOC 방식으로 커밋한다.

## 규칙

- `git add`, `git commit -a`, `git commit --all`은 절대 사용하지 않는다.
- staged 변경만 분석하고, unstaged 변경은 건드리지 않는다.
- HEREDOC 방식과 Co-Authored-By를 유지한다.
- API 키, 쿠키, 액세스 토큰 등 민감정보 포함 여부를 먼저 점검한다.

## 검증 체크리스트

- [ ] staged area만 분석했는가
- [ ] unstaged 변경을 건드리지 않았는가
- [ ] `git add`를 실행하지 않았는가
- [ ] 한국어 Conventional Commit 형식인가
- [ ] Co-Authored-By가 포함됐는가
