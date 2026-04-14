# tools-ai 인사이트

- 표본: `community/tools-ai` 최신 50개 + 오래된 30개 = 80개
- 빈도는 `문서 내 도구명 언급 여부` 기준이며, 한 글에 여러 도구가 나오면 중복 집계했다.

## 1. 도구별 언급 빈도

| 도구 | 언급 수 | 메모 |
| --- | ---: | --- |
| Claude Code | 10 | 코딩 성능 기준의 기본 비교축이다. |
| ChatGPT/GPT | 9 | 기획, 비교검증, 범용 질의용으로 많이 나온다. |
| Cursor | 8 | IDE로 가장 자연스럽게 언급된다. |
| Antigravity | 7 | 프론트/UI 생성 쪽 기대가 크다. |
| Gemini | 7 | 디자인, PRD, 대체 모델 용도로 같이 쓴다. |
| Codex | 3 | 백엔드/정교한 코드 작성 쪽으로 평가된다. |
| OpenClaw | 3 | 자동화/에이전트 실행 쪽 관심이 있다. |
| Netlify | 1 | 배포 질문에서만 드물게 나온다. |
| Supabase | 1 | 스택 예시로만 나온다. |
| n8n | 1 | 자동화 입문 키워드로만 나온다. |
| v0 | 1 | 프론트 초안 생성 도구로 나온다. |
| Bolt | 1 | 비교 대상 수준이다. |
| Lovable | 1 | 비교 대상 수준이다. |

## 2. 자주 쓰이는 도구 조합

표본 내 반복 조합과 대표 근거:

| 조합 | 관찰 | 출처 |
| --- | --- | --- |
| GPT/Gemini + v0 | PRD/기획은 GPT나 Gemini, 프론트 초안은 v0 | `보통 어떤 ai조합 사용하시나요?` (article_id: 1225) |
| Cursor + Next.js + Vercel | 구현과 배포를 한 묶음으로 인식 | `어떤 툴/언어 위주로 하시는지 궁금하네요` (article_id: 553) |
| Codex + Antigravity + Gemini Pro | 백엔드는 Codex, 프론트 IDE는 Antigravity, 모델은 Gemini Pro라는 명시적 추천 | `바이브 코딩 팁` (article_id: 227) |
| Cursor AI + GPT + Claude | 구현은 Cursor, 알고리즘은 GPT에서 Claude로 보완 | `코인 자동매매 프로그램 한 달 후기` (article_id: 782) |
| Antigravity + Cursor | 실제 첫 수익화 사례에서 함께 사용 | `홈페이지 작업으로 첫 수익화 성공!!` (article_id: 1071) |

짧은 근거 인용:

> "백엔드는 CODEX가 최고" (article_id: 227)

> "프론트의 경우 IDE 는 안티그래비티" (article_id: 227)

> "저는 gpt나 재미나이로 prd 작성하고 프론트는 주로 V0" (article_id: 1225)

## 3. 비용/불만 관련 언급

반복되는 불만은 세 가지다.

1. Claude 계열 비용이 부담된다.
   `Claude Code Max가 필요할까요? 가격이 좀 부담되네요.` (article_id: 6097)
2. 토큰이 빨리 닳는다.
   `토큰사용량이 생각보다 많네요` (article_id: 6676), `둘중 하나 요금제를 업그레이드` 고민 (article_id: 6933)
3. 도구가 중간에 엇나가거나 멈춘다.
   `안티그래비티는 ... 가끔 자기 혼자 만들다 말길래` (article_id: 553)
4. 초보자는 결과 통제가 어렵다.
   `내가 원하는 대로 만들어주지 않고` (article_id: 6749)

정리하면, 불만의 핵심은 단순 성능보다 `비용 대비 제어 가능성`이다.

## 4. 커뮤니티 표준 스택

표본을 종합하면 가장 흔한 표준 스택은 아래 흐름이다.

1. 기획: ChatGPT 또는 Gemini로 PRD, 아이디어 정리
2. 구현: Claude Code 또는 Cursor
3. 프론트 보강: Antigravity, v0
4. 버전관리: GitHub
5. 배포: Vercel 또는 Netlify

근거:

- `저는 gpt나 재미나이로 prd 작성` (article_id: 1225)
- `IDE는 커서 주로 쓰고` + `Next.js/Vercel` (article_id: 553)
- `무조건 git hub 를 사용하세요` (article_id: 227)

보완 해석:

- `Claude Code`는 성능 기준 기본값에 가깝다.
- `Cursor`는 가장 무난한 IDE 포지션이다.
- `Antigravity`는 프론트/UI 기대값이 높지만 신뢰성 불만도 같이 붙는다.
- `Codex`는 메인스트림은 아니지만 "백엔드 깔끔함" 이유로 강한 지지를 받는 소수파가 있다. (article_id: 227)
