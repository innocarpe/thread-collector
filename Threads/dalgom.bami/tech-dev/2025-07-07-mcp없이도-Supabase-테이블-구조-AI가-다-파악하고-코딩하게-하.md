---
username: dalgom.bami
category: 기술/개발
pk: 3671287949771286276
taken_at: 1751871649
date: 2025-07-07
source: https://www.threads.net/@dalgom.bami

labels: ["개발도구", "웹/SaaS", "AI/LLM"]---

# mcp없이도 Supabase 테이블 구조 AI가 다 파악하고 코딩하게 하기

mcp없이도 Supabase 테이블 구조 AI가 다 파악하고 코딩하게 하기

아래 명령어를 터미널에서 실행($PROJECT_REF는 본인 프로젝트 ID)
npx supabase gen types typescript --project-id "$PROJECT_REF" --schema public > database.types.ts

내가 정의한 테이블, 컬럼, 릴레이션 모두 Typescript type으로 정의된 파일 하나가 자동 생성 됨. 이 파일을 Context로 추가해주면 AI가 정확하게 내 데이터 구조를 파악하고 코딩 가능함

await supabase.createClient(....)를 이용해서 client생성을 할 때
위에서 생성된 Database를 아래와 같이 Generic에 넣어주면 데이터가 any타입이 아닌 제대로된 타입으로 옴
supabase.createClient<Database>

선행조건) supabase cli 설치,로그인 되어있어야 함(댓글 링크 문서 참고)
