# programmingzombie 블로그 인사이트 개요

## 기본 정보
- 총 글 수: 50편
- 분석 기간: 2015-11-18 ~ 2017-05-26
- 주요 카테고리 분포: `web-app` 33편, `dev-tools` 26편, `learning-retro` 12편, `productivity` 1편, `career-growth` 1편, `startup-philosophy` 1편

이 블로그는 안드로이드 실무 메모를 중심으로, 자바 백엔드, 개발 도구, 개인 학습 기록이 겹쳐 있는 개발 로그형 아카이브에 가깝다. 글의 상당수는 긴 이론 설명보다 "막혔던 문제를 어떻게 풀었는지"를 빠르게 남기는 방식으로 쓰였고, 실제 코드나 명령어, 설정 경로, 참고 링크가 바로 이어진다. 주제 분포를 보면 안드로이드 UI와 컴포넌트, SQLite와 소켓 같은 데이터 처리, 스레드와 스케줄링, ADB·SourceTree·IntelliJ 같은 도구 활용이 반복 축을 이룬다.

## 핵심 주제 Top 5
1. 안드로이드 UI와 컴포넌트 실전: Fragment, Navigation Drawer, ActionBar, RecyclerView, Snackbar, ripple effect처럼 화면 동작이 꼬이는 지점을 직접 해결한다. 대표 글은 `[안드로이드] Fragment BackStack에 대한 고찰.`, `RecyclerView 내부 CheckBox 체크 상태 유지시키기`이며 관련 글은 12편 안팎이다.
2. 데이터 저장과 네트워크 연동: SQLite 저장, DB 확인, MySQL 연동, 소켓 통신, ObjectMapper 기반 JSON 처리처럼 앱과 서버 사이의 데이터 흐름을 다룬다. 대표 글은 `[안드로이드] SQLite 사용하기`, `[안드로이드] 서버/클라이언트 소켓(Socket) 통신하기`이며 관련 글은 12편 안팎이다.
3. 동시성과 스케줄링: `Timer`, `ScheduledExecutorService`, `Callable`, `synchronized`, `InterruptedException`처럼 비동기 제어의 기본기를 반복해서 학습한다. 대표 글은 `Callable과 Thread`, `Thread.sleep throw InterruptedException?`이며 관련 글은 5편이다.
4. 도구·운영·디버깅: ADB, Ubuntu 서버, HeidiSQL, JUnit, SourceTree, IntelliJ 설정처럼 개발 환경을 바로 복구하거나 점검하는 팁이 많다. 대표 글은 `리눅스 서버 셋팅`, `[안드로이드] adb에서 apk version 확인하기`이며 관련 글은 9편 정도다.
5. 학습·커리어·협업 관점: 참고 링크 큐레이션, Trello 운영, 리쿠르팅 데이 후기처럼 공부 방식과 일하는 태도를 함께 기록한다. 대표 글은 `[Trello] 좋은 사이트 참고`, `구글 캠퍼스 리쿠르팅 데이 후기 (2017.05.25)`이며 관련 글은 15편 정도다.

## creator 특성
- 글쓰기 스타일: 문제 발생 상황을 먼저 적고, 바로 적용 가능한 코드·명령어·설정값으로 이어지는 메모형 실전 글쓰기가 두드러진다.
- 주요 관심사: 안드로이드 앱 개발, SQLite와 소켓 같은 로컬/네트워크 데이터 처리, 스레드 제어, 서버 셋업, 개발 생산성 도구.
- 반복 키워드: 안드로이드, SQLite, 서버, 소켓, Fragment, Timer, Thread, ADB, 퍼미션, 참고 자료.
- 전반적 성향: 공식 문서와 외부 블로그를 적극 참조하되, 결국은 "직접 막힌 문제를 다시 안 막히게 정리하는" 개인 지식베이스 구축형 개발자에 가깝다.

## 주목할 만한 인사이트
- 소프트웨어 엔지니어의 핵심은 기술 스택 자체보다 문제를 끝까지 해결하는 능력이라는 관점이 가장 선명하다. 출처: `2017-05-26-54-insight.md`
- `InterruptedException`를 무시하지 말고 인터럽트 상태를 복원해야 한다는 지적은, 단순 문법 메모를 넘어 안정적인 동시성 처리 원칙을 보여준다. 출처: `2016-01-07-11-insight.md`
- 여러 응답을 합쳐야 하는 상황에서는 `Thread`보다 `Callable`과 `Future.get()`으로 완료 시점을 제어해야 한다는 판단이 실무적이다. 출처: `2016-02-04-14-insight.md`
- `AppCompatActivity`에서는 `getSupportFragmentManager()`를 써야 BackStack이 제대로 동작한다는 정리는 안드로이드 호환성 이슈를 정확히 짚는다. 출처: `2016-03-10-23-insight.md`
- SQLite 기본 시간이 UTC로 저장돼 9시간 어긋날 수 있으니 `datetime('now','localtime')`를 써야 한다는 팁은 현업성 높은 장애 예방 지식이다. 출처: `2016-04-26-34-insight.md`
