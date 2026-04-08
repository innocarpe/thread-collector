---
username: dalgom.bami
category: 기술/개발
pk: 3820600553391692542
taken_at: 1769671099
date: 2026-01-29
source: https://www.threads.net/@dalgom.bami
---

# vercel에 next

vercel에 next.js 배포해서 무료 플랜으로 쓰고 있다면 1분 투자로 성능 바로 올릴 수 있음

setting - functions로 들어가서 보면 되고, 기본적으로 Washington, D.C., USA (East) - us-east-1 - iad1 로 세팅되어있고 무료플랜은 딱 1개의 region만 고를 수 있습니다. 

고객들이 워싱턴에 주로 살고 있는거 아니면 나에게 맞는 region으로 고르고 재배포 한번 진행하세요. 한국사용자 대상이면 Seoul, South Korea (Northeast) - ap-northeast-2 - icn1 골라야겠죠?

저는 next.js edge functions 전혀 안쓰는 간단한 페이지들이라구요? 그럴리가요 next.js는 아무리 간단한 웹이라도 이미지 최적화, 페이지 로딩등을 위해서 내부적으로 function 엄청 많이 씁니다.
