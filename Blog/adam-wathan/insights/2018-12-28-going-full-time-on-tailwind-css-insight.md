---
source: blog
creator: adam-wathan
url: https://adamwathan.me/going-full-time-on-tailwind-css
title: Going Full-Time on Tailwind CSS
published_at: 2018-12-28
collected_at: 2026-04-15
categories: ["startup-philosophy", "monetization", "case-study"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. Tailwind CSS는 1년 남짓한 기간 동안 빠르게 채택되었고, Adam Wathan은 이를 자신의 가장 큰 임팩트 프로젝트로 보고 2019년부터 전업으로 집중하기로 했다.
2. 전업 전환의 첫 우선순위는 v1.0 출시이며, 큰 변화보다 네이밍 일관성, 기본 설정 개선, 미래 기능을 위한 변경 정리에 집중한다.
3. 제품 성장의 핵심 수단으로 문서 확장, 무료 공식 비디오 코스, 커뮤니티 인프라 개선을 동시에 추진한다.
4. 커뮤니티가 만든 플러그인·사례·갤러리를 공식 채널에서 더 잘 보여주는 것이 채택 확대에 도움이 된다고 본다.
5. 장기 지속 가능성은 기존 교육 비즈니스 유지, 기업 스폰서십 가능성 검토, 테마·UI 킷 같은 프리미엄 제품으로 확보하려 한다.

## 공개된 숫자·지표
- 릴리스 수: 30회 (기간: 2017년 할로윈 밤 첫 공개 이후~2018-12-28, 출처: "We've published 30 releases")
- 코드베이스 기여자 수: 77명 (기간: 2017년 할로윈 밤 첫 공개 이후~2018-12-28, 출처: "77 people have contributed to the codebase")
- GitHub 스타 수: 8,000회 이상 (기간: 2018-12-28 기준, 출처: "has been starred over 8,000 times")
- Slack 커뮤니티 참여자 수: 1,100명 이상 (기간: 2018-12-28 기준, 출처: "Over 1,100 people joined the Tailwind CSS Slack community")
- Twitter 팔로워 수: 10,000명 이상 (기간: 2018-12-28 기준, 출처: "Over 10,000 people started following @tailwindcss on Twitter")
- npm 설치 수: 거의 700,000회 (기간: 2018-12-28 기준 누적, 출처: "The framework has been installed almost 700,000 times via npm")
- 출시 후 경과 기간: 1년 이상 (기간: 2017년 할로윈 밤 첫 공개 이후, 출처: "Tailwind has been out in the wild for over a year now")
- v1.0 준비 기간: 2019년 첫 한 달가량 (기간: 2019년 초, 출처: "The first month or so of 2019 is going to be dedicated")
- v1.0 출시 목표 시점: 2019년 2월 (기간: 2019-02, 출처: "There will be a v1.0.0 release in February for sure.")
- 포럼 운영 투입 시간: 매주 몇 시간 (기간: 2019년 예정, 출처: "I'm planning to spend a few hours every week")
- 무료 비디오 코스 목표 시점: 4월 또는 5월경 (기간: 2019년 봄, 출처: "I'm hoping to have it ready around April or May")
- 공식 테마·UI 킷 작업 시점: 봄과 여름 (기간: 2019년 봄~여름, 출처: "Over the spring and summer")
- 기존 코스 업데이트 목표: 2020년 Test-Driven Laravel 업데이트 (기간: 2020년, 출처: "I'm planning to release an updated version ... in 2020")
- Advanced Vue Component Design 업데이트 조건: Vue 3.0 출시 시점 (기간: 향후 Vue 3.0 출시 후, 출처: "when Vue 3.0 is released")
- 전업 실험 기간: 2019년 전체 (기간: 2019-01-01~2019-12-31, 출처: "I'm going to give it a shot for all of 2019")

## 언급된 도구·서비스
- Tailwind CSS: 빠르게 커스텀 UI를 개발하기 위한 utility-first CSS 프레임워크
- GitHub Releases: Tailwind CSS의 릴리스 이력을 공개하는 채널
- GitHub Contributors Graph: 코드베이스 기여자 수를 보여주는 지표 출처
- GitHub Repository: Tailwind CSS의 스타와 코드 협업이 일어나는 저장소
- Slack: Tailwind CSS 커뮤니티의 실시간 대화 공간으로 사용되던 채널
- Twitter: `@tailwindcss` 계정으로 사용자 기반 성장을 보여주는 채널
- npm: Tailwind CSS 설치 수를 보여주는 배포 채널
- Algolia: Tailwind 문서 검색을 지원하는 회사이자 Tailwind 적용 사례
- vue-cli: Tailwind 통합 문서화를 확장하려는 대상 빌드 도구
- nuxt.js: Tailwind 통합 문서화를 확장하려는 대상 프레임워크
- create-react-app: Tailwind 통합 문서화를 확장하려는 대상 도구
- next.js: Tailwind 통합 문서화를 확장하려는 대상 프레임워크
- Ember: Tailwind 통합 문서화를 확장하려는 대상 프레임워크
- Rails: Tailwind 통합 문서화를 확장하려는 대상 프레임워크
- Phoenix: Tailwind 통합 문서화를 확장하려는 대상 프레임워크
- Discourse: 기존 GitHub Discussions 대체용 정식 포럼 후보
- Discord: Slack 커뮤니티를 이전하려는 실시간 커뮤니티 플랫폼
- CSS Grid: 향후 추가를 고려하는 핵심 기능
- `@apply`: hover 같은 utility variant와 함께 동작하도록 개선하려는 기능
- Style guide generator: Tailwind config 기반으로 만들고 싶은 추가 도구
- Playground/Sandbox: JSFiddle/CodePen 스타일 데모 제작을 위한 추가 도구 아이디어
- JSFiddle: 데모 제작 경험의 비교 기준
- CodePen: 데모 제작 경험의 비교 기준
- Bootstrap Theme Store: 유료 테마 판매 모델의 참고 사례
- Test-Driven Laravel: 기존 교육 비즈니스에서 계속 운영할 코스
- Advanced Vue Component Design: Vue 3.0 시점에 업데이트하려는 기존 코스

## 언급된 다른 creator·앱
- Derek Sivers: `Anything You Want`를 통해 자신의 일의 공통 목적을 재정리하는 계기를 준 인물
- Algolia: Tailwind 문서 검색을 지원하고 Tailwind로 새 문서 사이트를 만든 회사
- Statamic: Slack에서 Discord로 이전한 커뮤니티 성공 사례
- EmberJS: Discord 이전 성공 사례로 언급된 커뮤니티
- Steve Schoger: 공식 테마와 UI 킷을 함께 만들 예정인 협업자
- Evan You: Vue.js 개발을 기업 후원으로 지속한 참고 사례
- Vue.js: 기업 스폰서십 모델의 참고 대상 프로젝트
- Taylor Otwell: Laravel 개발을 기업 후원으로 지속한 참고 사례
- Laravel: 기업 스폰서십 모델의 참고 대상 프로젝트
- awesome-tailwindcss: 커뮤니티가 만든 Tailwind 큐레이션 프로젝트
- Built with Tailwind: Tailwind 사이트 사례를 모아두는 커뮤니티 프로젝트
- TailwindComponents: Tailwind 컴포넌트와 플러그인을 큐레이션하는 커뮤니티 프로젝트
- Bootstrap: 공식 테마 스토어를 운영하는 유료 제품화 참고 사례

## 복제 가능한 전술 (≤3)
1. 전업 전환 또는 핵심 프로젝트 집중 선언과 함께 1년짜리 실행 로드맵을 공개한다.
   - 구체적 스텝: 현재까지의 성장 지표를 정리한다. 프로젝트의 장기 목적을 한 문장으로 명확히 정의한다. 다음 1년의 우선순위를 출시, 문서, 교육, 커뮤니티, 수익화 순으로 공개한다. 각 항목에 대략적인 시점을 붙여 기대치를 맞춘다.
   - 예상 리소스: 창업자 1명, 기존 지표 접근 권한, 공개 로드맵을 게시할 블로그 또는 제품 사이트
   - 예상 효과: 사용자에게 프로젝트의 진지함과 지속 의지를 전달하고, 채택과 커뮤니티 참여를 더 끌어올릴 기반을 만든다.
2. 메이저 버전 출시 직후 문서와 무료 교육 콘텐츠를 연속 배치해 진입장벽을 낮춘다.
   - 구체적 스텝: 먼저 API 문서의 미완성 페이지를 끝낸다. 이어 튜토리얼형 문서, 컴포넌트 예시, FAQ 성격의 지식베이스를 추가한다. 문서가 안정되면 공식 무료 비디오 코스를 만들어 실제 인터페이스 제작 과정을 보여준다.
   - 예상 리소스: 문서 사이트, 예제 제작 시간, 영상 제작 도구
   - 예상 효과: 기능 설명을 넘어 실제 사용법까지 제공해 신규 사용자의 학습 비용을 줄이고, 제품 채택 확대로 연결할 수 있다.
3. 실시간 채팅과 비동기 포럼을 분리하고, 공식 큐레이션 허브로 생태계를 노출한다.
   - 구체적 스텝: 질문이 누적되는 정식 포럼을 연다. 창업자가 매주 직접 답변하는 시간을 확보한다. 실시간 채널은 Discord 같은 별도 공간으로 운영한다. 공식 사이트에 플러그인, 도구, 구축 사례 갤러리 섹션을 추가해 커뮤니티 산출물을 연결한다.
   - 예상 리소스: 포럼 소프트웨어, 채팅 플랫폼, 운영자 응답 시간, 웹사이트 큐레이션 섹션
   - 예상 효과: Slack처럼 답변이 흘러가 버리는 문제를 줄이고, 커뮤니티 산출물을 공식적으로 보여줘 채택 증가에 도움을 준다.

## 원문 요약 (≤5문장)
Adam Wathan은 Tailwind CSS가 지난 1년여 동안 빠르게 성장했고, 자신이 사람들의 소프트웨어 개발을 돕는다는 장기 목표를 가장 크게 실현할 수 있는 프로젝트라고 판단해 2019년부터 전업으로 집중하겠다고 밝혔다. 우선순위는 2019년 초 v1.0 출시, 미완성 문서 보강, 무료 공식 비디오 코스 제작이다. 동시에 GitHub 기반 논의를 정식 포럼으로 옮기고 Slack에서 Discord로 이전하는 등 커뮤니티 운영 구조도 손보려 한다. 공식 사이트에서 플러그인과 구축 사례를 더 적극적으로 소개하고, CSS Grid 같은 새 기능과 부가 도구도 검토한다. 수익화는 기존 교육 비즈니스 유지, 기업 스폰서십 가능성, 테마·UI 킷 같은 프리미엄 제품으로 장기 지속 가능성을 확보하는 방향이다.

## 본문 포인트별 발췌
> So starting in 2019, I'm going to be working full-time on Tailwind CSS.
> There will be a v1.0.0 release in February for sure.
> It will be completely free
> I'm planning to spend a few hours every week making sure everyone's questions are answered
> Either way, I'm going to give it a shot for all of 2019 and see what I can do.
