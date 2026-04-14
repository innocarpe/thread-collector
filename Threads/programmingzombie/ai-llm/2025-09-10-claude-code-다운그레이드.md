---
pk: "3718564764437388484"
username: "@programmingzombie"
category: "미분류"
taken_at: 1757507485
date: "2025-09-10"
source: "https://www.threads.net/@programmingzombie"
chain_pks: ["3718564764437388484", "3718564809433897295"]

labels: ["AI/LLM", "제품전략", "앱개발"]
---

# Claude Code 다운그레이드

Claude Code 다운그레이드

버전 1.0.88로 다운그레이드 하면 성능이 예전처럼 좋아진다는 글이 보여서 버전 다운그레이드 진행했습니다. 구독남은 11일동안 열심히 써보고 후기 올리겠습니다. 🫡

다운그레이드 방법
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code@1.0.88

brew
brew uninstall claude-code
brew install claude-code@1.0.88

이후 자동 업데이트 비활성화 처리하기
vim ~/.claude/settings.json 로 json 파일 열고 아래 키 값 추가하기(스크린샷 참고)
"DISABLE_AUTOUPDATER": "1"

저의 경우 이상하게 설치를 했는지 npm uninstall이 안되서 강제로 폴더 싹다 지우고 캐시 날리는 작업을 했는데, MCP까지 모두 날라가서 https://smithery.ai/ 에 들어가서 아래 MCP 설정을 추가했습니다. 예전에는 Claude Code MCP 연결이 잘 안됐었는데 이제 되게 편리하게 잘 됩니다. 명령어 복사 붙혀넣기 후 Claude 들어가서 /mcp 명령어 입력후 연결만 하면 끝!
