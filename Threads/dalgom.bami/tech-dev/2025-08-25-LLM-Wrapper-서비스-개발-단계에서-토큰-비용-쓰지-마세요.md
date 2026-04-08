---
username: dalgom.bami
category: 기술/개발
pk: 3706782030141647898
taken_at: 1756102874
date: 2025-08-25
source: https://www.threads.net/@dalgom.bami
---

# LLM Wrapper 서비스 개발 단계에서 토큰 비용 쓰지 마세요

LLM Wrapper 서비스 개발 단계에서 토큰 비용 쓰지 마세요

구글 ai studio 접속해서 우측 상단 Get api key 눌러서 발급받으면 무료 등급 api 키를 받을 수 있는데 (카드 등록 필요 없음 구글 로그인만 필요)

Gemini 2.5 pro를 아래의 limit조건으로 매일 무료로 쓸 수 있습니다.
RPM(1분당 호출 수) = 5
TPM(1분당 입력 토큰 수) = 250,000
RPD(하루 호출 수) = 100

참고로 API 키 별로 할당량이 세팅되며, 한 계정이 여러 API키를 생성할 수도 있고, 구글 계정 여러개를 활용할 수도 있습니다..만 1개로도 그럭저럭 개발할만했습니다. 

Gemini 2.5 pro의 성능이 아쉽다면, 일단 개발은 Gemini 2.5 pro, flash를 이용해 진행하고 추후 완성 되었을 때 선호하는 언어모델 API로 교체할 수 있게 짜두면 됩니다.

이 부분을 코드에서 추상화해두면 나중에 바꿀때 편하겠죠?
