---
username: dalgom.bami
category: 기술/개발
pk: 3667540634912732430
taken_at: 1751424935
date: 2025-07-02
source: https://www.threads.net/@dalgom.bami

labels: ["앱개발", "웹/SaaS", "AI/LLM"]---

# Supabase의 anonymous login 기능을 활용하는 방법이야

Supabase의 anonymous login 기능을 활용하는 방법이야.

signInAnonymously 함수는 호출되면 사용자의 기기 정보 등 여러가지를 조합해 임의의 해시값을 하나 만들고 supabase 로그인 상태로 만들어줘. 

이제 사용자가 로그인 상태이므로 RLS도 다 적용할 수 있게 되지. 사용자별로 id가 발급이 되었을 거거든. 즉 이 기기를 쓰는 사람이 아니면 서버쪽 데이터에 절대로 접근할 수 없어. 보통 로그인 없이 구현하다보면 이 부분에서 보안 구멍이 생기기 쉽거든

주의해야할 점은 사용자가 로그아웃 하거나 기기를 지우면 해당 아이디로 다시는 로그인 못한다는 점이 있어.

그리고 개발 실수도 signInAnonymously 함수를 또 호출하게 되면 이전 id는 날아가게 돼.

로그인 세션 여부를 파악하고, 세션이 없을 때만 위 로직을 실행해줘야 해.
앱 껐다켜도 로그인 유지를 위해 init때 persistSession, async storage를 써야겠지?
