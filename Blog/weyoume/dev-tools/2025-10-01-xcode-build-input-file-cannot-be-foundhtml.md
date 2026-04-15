---
source: blog
creator: weyoume
url: https://mydevspace.blogspot.com/2025/10/xcode-build-input-file-cannot-be-found.html
title: "Xcode \"Build input file cannot be found\" 에러 발생"
published_at: 2025-10-01
collected_at: 2026-04-15
author: ""
lang: ko
categories: ["dev-tools"]
extras:
  word_count: 796
  adapter: rss
---

[기본 콘텐츠로 건너뛰기](#main)

### [2025년 9월 카카오 사태 프로필 미공개](https://mydevspace.blogspot.com/2025/10/2025-9.html)

[10월 01, 2025](https://mydevspace.blogspot.com/2025/10/2025-9.html)

2025년 9월 23일 카카오 사태가 벌어졌다.   나는 다행히 앱스토어 설정에 들어가서 자동업데이트를 비활성해서 이번 사태를 잠깐 피해갈 수 있었다.   하지만 유튜브를 보다보니까   이번에 업데이트를 이미 한 사람들에게 나의 프로필이 까발려 진다는 것을 알게되었다.   내 친구한테 알려지는 건 좋은데   카카오톡은 내가 전혀 모르는 사람이나 싫은 사람, 업무적인 사람들 연락처에 있는 모든 사람이나 전화 번호가 변경되서 모르는 사람들도 친구 목록에 표시가 된다.   그런 모든 사람들에게 내 사생활을 강제로 공개되도록 해버렸다는 거에 공포를 느꼈다.   프로필 탭으로 이동해서   내 프로필에서 오른쪽 상단에 설정 버튼이 있고 그걸 클릭하면   프로필 설정들이 있고 거기서 옵션들을 비활성 해주자   “프로필 인증배지 표시”, “내 프로필 검색”, “내 홈 표시” 모두 비활성 해줬다.   솔직히 앞으로 이번 사태 이전으로 롤백을 시키지 않는한 앞으로 프로필에 사진을 올릴거 같지 않다.   이미 앱은 배포가 되었고   이 사태가 벌어진 버전의 앱을 업데이트 하지 않고 사용하는 사람들이 많을것이다.   (보통은 앱을 배포 하고 강제로 업데이트 유도하지 않는 이상 앱을 업데이트 하지 않는 사람들이 많다.) 만약에 더 프로필 공개에 공포를 느낀다면 프로필에 올린 이미지들을 당장 지우자.   *추가* 숏폼과 오픈채팅을 합쳐놓은 것도 참 거지같은 짓을 한거라고 생각한다.   오픈채팅에 개발이나 다이어트나 여러가지 같은 관심을 가진 사람들이 단체 톡방에 들어가서 커뮤니티를 하고 계실거다.   나도 개발 단체톡방에 들어가서 대화를 하는데   왜 그걸 합쳐놔서   오픈채팅을 들어가기 위해서 무조건 숏폼을 강제로 봐야 한다는 건 참 별로다.   *추가 2* 벌서 온갖 야시시 하고 폭력적인 숏폼에 노출되고 있...

공유

- 

공유 링크 만들기

- 

Facebook

- 

X

- 

Pinterest

- 

이메일

- 

기타 앱

### 
Xcode "Build input file cannot be found" 에러 발생

[10월 01, 2025](https://mydevspace.blogspot.com/2025/10/xcode-build-input-file-cannot-be-found.html)

Xcode 를 사용해서 개발을 하면서 특정 파일에서 "Build input file cannot be found" 오류가 발생하는 경우가 있다   
이 오류를 해결하는 여러가지 방법을 구글링을 하면서 찾을 수 있지만   
해당 파일의 경로가 문제인 경우가 있다.   
실제 파일이 정상적으로 프로젝트에 포함되어 있고   
Xcode 를 Clear 하거나 Full Clear 해도 계속 같은 오류가 발생한다면   
Xcode 에서 해당 파일을 클릭 한 후에 Xcode 화면 오른쪽에 파일의 경로 Location 과 Full Path 를 확인할 수가 있는데   
거기에서 Location 이 다른 파일들과 다르게 설정이 되어 있는 경우 저런 특정 파일을 찾을 수 없다는 오류가 발생하게 된다. 

공유

- 

공유 링크 만들기

- 

Facebook

- 

X

- 

Pinterest

- 

이메일

- 

기타 앱

### 태그

[iOS](https://mydevspace.blogspot.com/search/label/iOS)

라벨:
[iOS](https://mydevspace.blogspot.com/search/label/iOS)

공유

- 

공유 링크 만들기

- 

Facebook

- 

X

- 

Pinterest

- 

이메일

- 

기타 앱

### 
이 블로그의 인기 게시물

### 
[애드몹 계정 정지 최대한 방지 하는 방법 (나의 생각)](https://mydevspace.blogspot.com/2023/04/blog-post.html)

[4월 18, 2023](https://mydevspace.blogspot.com/2023/04/blog-post.html)

아직까지는 앱에서 계정 정지가 당하는 사태가 오지 않았지만   주변에 애드몹 계정 정지를 당하는 사태가 아직도 빈번하게 발생을 해서 글을 적어 본다.   1. 테스트 광고 id 사용  ! https://developers.google.com/admob/ios/test-ads?hl=ko   위 사이트 보며 데모 광고 id 가 광고 종류 별로 존재한다.   앱코드에서 개발 모드와 배포 모드로 분기를 할 수 있다면   개발 모드에서는 저 데모 광고 id 를 적용해서 항상 어느 상황이던 데모 광고가 표시되도록 하는게 좋지 않을까 싶다.   2. 테스트 디바이스 id 사용   앱 빌드 하면 로그 창에 테스트 디바이스 id 를 등록하라고 특정 글자가 표시된다.   그걸 아래와 같은 함수에 적용 해주면 테스트 광고가 표시된다.   GADMobileAds.sharedInstance().requestConfiguration.testDeviceIdentifiers   예전 광고 UDID 이슈가 없을 때는 괜찮았는데   요즘은 저 거만 너무 믿으면 저거 적용하기 전에 일반 광고가 표시될 가능성이 높고   저게 주기적으로 빌드하면서 랜덤하게 계속 바뀌어서 엄청 불편하다. 그래서 나는 어느 순간 부터는 저거는 그냥 무시하고 안쓰는 편이고 다음 테스트기기 등록을 하는 편이 더 좋다.   3. 테스트 기기 등록  !!! 애드몹 웹사이트로 이동하면   좌측 메뉴 중에 “설정” - “기기 테스트” 항목에 애플/안드로이드 기기의 광고 ID 를 등록할 수 있다.   등록을 하면 앱 실행 시 바로 광고 ID 가 표시된다.   iOS 경우에는 IDFA 허용 팝업 이후에 테스트 광고가 표시되니까   개인적으로 iOS 개발의 경우에는 처음 앱 실행하고 광고 요청 자체를 IDFA 광고 팝업 후에 하는 것도 좋지 않을까 싶다.  ...

공유

- 

공유 링크 만들기

- 

Facebook

- 

X

- 

Pinterest

- 

이메일

- 

기타 앱

[자세한 내용 보기](https://mydevspace.blogspot.com/2023/04/blog-post.html)

### 
[아이폰/아이패드 하단 홈바 가리기 (특정 앱에서)](https://mydevspace.blogspot.com/2023/01/blog-post_4.html)

[1월 05, 2023](https://mydevspace.blogspot.com/2023/01/blog-post_4.html)

아이폰이나 아이패드를 사용하면서 앱에서 화면을 장시간 보는 경우  하단의 홈바가 눈에 거슬릴 때가 있다.  그 경우 설정의 "사용법 유도" 기능을 활용하면 화면에서 안보이게 할 수 있다.  이 기능의 경우는 모든 화면에서는 안되는거 같고 특정앱에서 화면의 특정부위를 안보이도록 하는 기능이다.  기기 홈화면의 설정으로 들어가서  "손쉬운 사용" - "사용법 유도" 에서  "사용법 유도" 를 활성화 하면 된다.  활성화 후에 특정 앱을 실행 한 후  오른쪽 전원버튼을 3번 클릭하면  사라지게할 영역을 그리고 활성화 하면  그 부분이 사라진 것을 볼 수 있다.  다시 사용중인 사용법 유도 기능을 비활성하거나 위치를 바꾸려면  오른쪽 전원버튼을 3번 클릭하면 된다. 

공유

- 

공유 링크 만들기

- 

Facebook

- 

X

- 

Pinterest

- 

이메일

- 

기타 앱

[자세한 내용 보기](https://mydevspace.blogspot.com/2023/01/blog-post_4.html)

### 
[애드몹(AdMob) 앱 광고 수익 2023년 1월 $4000](https://mydevspace.blogspot.com/2023/02/admob-2023-1.html)

[2월 07, 2023](https://mydevspace.blogspot.com/2023/02/admob-2023-1.html)

애드몹(AdMob) 앱 광고 수익 2023년 1월 2023 년 새해 첫 애드몹 수익이 나왔습니다.  저번달 보다 클릭 수는 증가했는데  수익은 줄어든게 좀 인상 깊내요.  전반적으로 대부분의 항목이 많이 줄어들었습니다. 

공유

- 

공유 링크 만들기

- 

Facebook

- 

X

- 

Pinterest

- 

이메일

- 

기타 앱

[자세한 내용 보기](https://mydevspace.blogspot.com/2023/02/admob-2023-1.html)