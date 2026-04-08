---
username: dalgom.bami
category: 기술/개발
pk: 3669051717829789854
taken_at: 1751605070
date: 2025-07-04
source: https://www.threads.net/@dalgom.bami
---

# 테스트로만 쓰던 supabase queue를 이번에 제대로 써보고 있는데 진짜 괜찮은 것 같아

테스트로만 쓰던 supabase queue를 이번에 제대로 써보고 있는데 진짜 괜찮은 것 같아

가장 마음에 드는 부분은 supabase는 로컬에서도 띄워서 쓸 수 있어서 개발환경으로 쓰고 있는데 이 로컬환경에서도 queue가 잘 된다는거..!

aws의 sqs 같은걸 쓸 땐 로컬에서 띄울 수가 없어서 불편한게 참 많았는데 로컬에서 queue관련 테스트도 다 빡세게 하고 운영 배포할 수 있는 좋은 세상이 됐네

queue + cron(supabase에서 됨) + edge function으로 배치잡을 굉장히 쉽게 할 수 있고 오래걸리는 작업은 queue + worker(supabase외부 별도 어플리케이션) 조합으로 쉽게 날먹이 가능함
