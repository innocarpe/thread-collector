---
username: dalgom.bami
category: 기술/개발
pk: 3717877759395147843
taken_at: 1757425588
date: 2025-09-09
source: https://www.threads.net/@dalgom.bami
---

# 그리고 RLS의 단점은 이걸 migration 코드로 db에 쿼리를 날려서 적용해야된다는 것임

그리고 RLS의 단점은 이걸 migration 코드로 db에 쿼리를 날려서 적용해야된다는 것임. 코드 베이스로 유지보수가 불가능하기 때문에 ai 툴이 기존에 어떻게 구현되어있는지 보려면 최신 코드 하나만 딱 보면 되는게 아니고 기존 마에그레이션 코드들을 둘러보며 파악해야된다는 것임.

그나마 이것도 rls를 supabase dashboard web ui에서 세팅한게 아닌 직접 migration 파일 만들어가며 관리했을 경우에나 가능함.

이 단점은 추후 설명할 trigger, RPC(트랜잭션이나 복잡한 쿼리 용 postgresql 함수) 등에도 똑같이 적용되며, ai 코딩툴은 복잡한 기능을 구현할 때 점점 RLS, trigger, RPC를 남발해서 유지보수가 아예 불가능할 정도의 코드, 기존 데이터가 손실될만한 코드를 무지성으로 찍어내기 시작함

분량조절에 실패해서 다음 이시간에 이어서..
