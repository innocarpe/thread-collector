---
username: dalgom.bami
category: 기술/개발
pk: 3666170129102387848
taken_at: 1751261558
date: 2025-06-30
source: https://www.threads.net/@dalgom.bami
---

# supabase 써서 ai wrapper만들 때 주의할 점

supabase 써서 ai wrapper만들 때 주의할 점

생각보다 초반에 스택 선정할 때 부터 고려해야되는 중요한 부분인데 놓치는 사람들이 많아서 정리해봄

외부 ai api와 연결하는 경우 보안을 위해 Edge function을 wrapping하게 되는데 edge function은 아래와 같은 제약이 있음

free: 150초, pro: 400초간 worker가 떠있음. 즉 이 시간 내에 다시 요청 시 조금 더 빠른 응답이 올 수 있음(warm상태)

(❗중요) free,pro상관 없이 한 건당 150초가 지나면 응답 끊김
이게 왜 중요하냐면 외부 ai api는 긴 텍스트 응답이나, 이미지, 영상 생성 등이 포함되면 응답이 더 오래걸리는 경우도 많기 때문에 150초 한번씩 넘을 것 같으면 쓰면 안 됨

(❗중요2) 한 번의 요청 당 cpu time은 2초까지만 허용됨
Async/await 하는 시간은 포함 안 됨. 순수 cpu 사용 시간
복잡한 연산 포함 안하는것을 추천
