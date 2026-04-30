# programmingzombie 블로그 인사이트 개요

## 기본 정보
- 총 글 수: 50편(요청 목록 기준)
- 분석 기간: 2015-11-18 ~ 2017-05-26
- 주요 카테고리 분포: `web-app` 33건, `dev-tools` 26건, `learning-retro` 12건, `career-growth` 1건, `productivity` 1건, `startup-philosophy` 1건

## 핵심 주제 Top 5
1. 안드로이드 UI·앱 구현: 프래그먼트, 레이아웃, 액션바, RecyclerView 같은 화면 단위 구현 이슈를 반복적으로 다룬다. 앱을 “직접 부딪혀 고치는” 실전 메모 성격이 강하다. — 17편, 대표 글: `RecyclerView 내부 CheckBox 체크 상태 유지시키기`
2. 자바 언어·동시성: `Timer`, `ScheduledExecutorService`, `Callable`, `synchronized`처럼 실행 제어와 스레드 안전성 문제를 꾸준히 파고든다. 동작 원리보다 실무에서 덜 사고 나는 선택지를 찾는 관점이 선명하다. — 8편, 대표 글: `스레드 동기화 synchronized에 관해서`
3. 도구·학습 자료 탐색: Handlebars, JavaScript 학습 사이트, SourceTree, IntelliJ, 유용한 블로그처럼 학습 효율을 높이는 외부 자료 공유가 잦다. 혼자 빠르게 흡수할 수 있는 레퍼런스를 중요하게 본다. — 7편, 대표 글: `HandleBar JS 알아보기`
4. 백엔드·서버 환경구축: 리눅스 서버 셋팅, Spring Boot 초기 설정, MySQL 연동, JDBC, 트랜잭션 등 안드로이드 밖의 서버 스택까지 학습 범위를 넓힌다. 모바일 개발자에 머무르지 않으려는 의지가 보인다. — 6편, 대표 글: `[Spring] @Transactional 에 관해`
5. 데이터 저장·디버깅: SQLite 저장, 조회, 시간대 보정, 데이터 추출처럼 “보관한 데이터가 실제로 어떻게 보이느냐”에 집착한다. 구현보다 검증과 확인 루프를 중시하는 주제다. — 4편, 대표 글: `[안드로이드] SQLite 사용하기`

## creator 특성
- 글쓰기 스타일은 길게 설명하는 튜토리얼보다 짧은 문제 해결 메모에 가깝다. “막혔다 → 찾았다 → 적용했다” 구조가 많고, Stack Overflow·외부 블로그·공식 문서를 빠르게 연결한다.
- 주요 관심사는 안드로이드 실전 개발, 자바 동시성, SQLite, 네트워크, 테스트 환경, 서버 설정으로 이어진다. 특히 개인 앱 개발 중 마주친 자잘하지만 치명적인 오류를 바로 기록하는 습관이 강하다.
- 반복 키워드는 `안드로이드`, `Java`, `SQLite`, `Fragment`, `서버`, `테스트`, `권한`, `네트워크`다. 전반적으로 “동작하게 만들고, 다시 재현 가능하게 정리하는 개발자”에 가깝다.

## 주목할 만한 인사이트
- 여러 주기 작업을 관리할 때는 `Timer`보다 `ScheduledExecutorService`가 종료 제어와 확장성 면에서 낫다는 판단을 남겼다. 출처: `2016-01-04-9-insight.md`
- 안드로이드 SQLite는 `SQLiteOpenHelper`를 싱글턴으로 감싸 CRUD를 공용화하면 여러 액티비티에서 재사용하기 좋다고 정리했다. 출처: `2016-03-04-21-insight.md`
- SQLite의 `datetime('now')`가 UTC 기준이라 9시간 오차를 만들 수 있으므로 `datetime('now','localtime')`를 써야 한다는 실전 팁이 눈에 띈다. 출처: `2016-04-26-34-insight.md`
- RecyclerView의 체크 상태 유실은 `setOnCheckedChangeListener(null)` 이후 `setChecked()`를 호출하는 순서로 해결할 수 있다고 정리했다. 출처: `2017-05-18-53-insight.md`
- 기술보다 문제 해결이 개발자의 본질이며, 커리어에서도 약점 보완보다 강점 언어화가 중요하다는 관점을 제시했다. 출처: `2017-05-26-54-insight.md`

## 2026-04-29 Play/web 역추적 업데이트
- 블로그/Threads 기반 정성 인사이트와 별개로, Google Play 상세 페이지의 **사업자번호·주소 fingerprint**(`765-19-02261`, `2025-경기김포-0251`, `김포한강2로 361`, `707동 2104호`)를 기준으로 앱을 역추적한 결과 **기존 Dave's / Rich Kim 외에 `DeveloperKhy`, `developerdoga` 라벨**이 추가로 드러났다.
- 이 방식으로 현재 공개 Play에서 **약 50개 Android 앱 노출**을 재확인했다. 최고 공개 설치 버킷은 `100K+`이며, 확인된 상위 앱은 `com.dave.keywordhelper`(스마트스토어 쇼핑몰 키워드 순위 분석), `com.dave.spellchecker`(맞춤법 검사기 / 띄어쓰기), `com.dave.soul.exchange_app`(환율알리미)다.
- 반대로, **2026-04-29 시점 공개 Play에서는 아직 `1M+` 설치 앱을 확인하지 못했다.** 따라서 이후 조사 원칙은 기존 계정과의 연관성을 먼저 가정하기보다, **`1M+ Android 앱 목록을 먼저 대량 스캔한 뒤 fingerprint로 역추적**하는 방향이 더 적절하다.
