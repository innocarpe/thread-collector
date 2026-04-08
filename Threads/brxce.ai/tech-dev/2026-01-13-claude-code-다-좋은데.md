---
pk: "3808868821432989402"
username: "@brxce.ai"
category: "기술/개발"
taken_at: 1768273139
date: "2026-01-13"
source: "https://www.threads.net/@brxce.ai"
chain_pks: ["3808868821432989402", "3808874918617187834", "3808875874046079242"]

labels: ["AI/LLM", "성장전략", "인디해킹"]---

# Claude Code 다 좋은데

Claude Code 다 좋은데
계속 컨텍스트 compacting 하는 거 짜증나지 않어?

클코 쓴다면 Serena 플러그인은 진짜 필수여.

코드베이스 시맨틱 검색해주는데,
이거 붙이고 나서 compact 시작하는 시간이
체감상 3배 이상 늘어남.

토큰 사용량도 반토막 이상 줄어든 듯.

나 혼자 $200짜리 계정 2개 쓰고 있었는데
지금은 1개도 남아도네.

OpenCode다 뭐다 요새 핫하던데
튜닝의 끝은 순정이라고 
나는 일단 클코만해도 기능 100% 활용 못하고 있다 생각해

*사용 방법 :

/plugin 들어가서 serena 설치하고.
클로드 코드한테 "serena 온보딩 + 인덱싱 해줘" 라고 요구하면 온보딩 진행할거야.
이후 "serena 프로젝트 활성화 해" 라고 명시적으로 요청하던지. 아니면 나같은 경우 CLAUDE.md 에 다음과 같이 박아 넣고 사용 중:

Serena Usage (MANDATORY)
Always use serena MCP tools:
find_symbol: Locate classes, functions, variables
get_symbols_overview: Understand file structure
find_referencing_symbols: Check dependencies before changes
insert_after_symbol / insert_before_symbol: For code insertion
replace_symbol: For refactoring
Never use grep/ripgrep when serena can do semantic search.
Never read entire files - use serena to get relevant symbols only.
