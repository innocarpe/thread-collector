---
source: blog
creator: weyoume
url: https://mydevspace.blogspot.com/2025/03/non-constant-range-argument-must-be.html
title: "Non-constant range: argument must be an integer literal 경고 해결법"
published_at: 2025-03-10
collected_at: 2026-04-15
author: ""
lang: en
categories: ["dev-tools"]
extras:
  word_count: 119
  adapter: rss
---

### 
Non-constant range: argument must be an integer literal 경고 해결법 

[3월 10, 2025](https://mydevspace.blogspot.com/2025/03/non-constant-range-argument-must-be.html)

최근에 기존 프로젝트를 Swift 6 으로 변경하는 작업을 계속 하면서 새롭게 발생하는 오류/경고인 "Non-constant range: argument must be an integer literal" 해결 방법을 정리해봤다. 

  

ForEach(0 ..< Define.ListTotal) { indexInt in

            inListView(indexInt)

}

  

위와 같은 코드에서 ForEach 부분에서 "Non-constant range: argument must be an integer literal" 경고가 발생하는데 

  

아래 코드와 같이 ForEach 조건문 뒤에 id:\.self 를 추가해주면 경고가 사라진다. 

  

ForEach(0 ..< Define.ListTotal, **id: \.self**) { indexInt in 

            inListView(indexInt)

}

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