---
source: blog
creator: weyoume
url: https://mydevspace.blogspot.com/2025/03/non-constant-range-argument-must-be.html
title: Non-constant range: argument must be an integer literal 경고 해결법
published_at: 2025-03-10
collected_at: 2026-04-15
categories: ["dev-tools"]
insight_extracted_at: 2026-04-15
---

## 핵심 주장 (≤5)
1. 기존 프로젝트를 Swift 6으로 변경하는 과정에서 `"Non-constant range: argument must be an integer literal"` 경고가 새롭게 발생할 수 있다.
2. `ForEach(0 ..< Define.ListTotal) { ... }` 형태의 코드에서 `ForEach` 부분에 해당 경고가 발생한다.
3. `ForEach` 조건문 뒤에 `id: \.self`를 추가하면 해당 경고가 사라진다.

## 공개된 숫자·지표
- 없음

## 언급된 도구·서비스
- Swift 6: 기존 프로젝트를 변경하는 과정에서 경고가 발생한 개발 환경으로 언급됨
- ForEach: 범위 기반 반복 UI 코드를 작성할 때 경고가 발생한 구문으로 언급됨
- `id: \.self`: `ForEach`에 추가해 경고를 제거하는 해결 방법으로 사용됨

## 언급된 다른 creator·앱
- 없음

## 복제 가능한 전술 (≤3)
1. Swift 6 전환 중 범위 기반 `ForEach` 경고를 식별하고 `id: \.self`를 추가해 해결한다.
   - 구체적 스텝: `ForEach(0 ..< someCount) { ... }` 형태의 코드를 찾고, 경고가 나는 구문을 `ForEach(0 ..< someCount, id: \.self) { ... }`로 수정한 뒤 빌드하여 경고 해소 여부를 확인한다.
   - 예상 리소스: Swift 프로젝트, 코드 검색 도구, 빌드 확인 시간
   - 예상 효과: 원문 기준으로 `"Non-constant range: argument must be an integer literal"` 경고가 사라진다.

## 원문 요약 (≤5문장)
글은 Swift 6으로 기존 프로젝트를 전환하는 과정에서 발생한 `Non-constant range: argument must be an integer literal` 경고의 해결법을 짧게 정리한다. 작성자는 `ForEach(0 ..< Define.ListTotal)` 구문에서 경고가 발생했다고 설명한다. 해결 방법은 `ForEach` 조건문 뒤에 `id: \.self`를 추가하는 것이다. 이 수정 후 경고가 사라진다고 정리한다.

## 본문 포인트별 발췌
> 최근에 기존 프로젝트를 Swift 6 으로 변경하는 작업을 계속 하면서 새롭게 발생하는 오류/경고인 "Non-constant range: argument must be an integer literal" 해결 방법을 정리해봤다.
> 위와 같은 코드에서 ForEach 부분에서 "Non-constant range: argument must be an integer literal" 경고가 발생하는데
> 아래 코드와 같이 ForEach 조건문 뒤에 id:\.self 를 추가해주면 경고가 사라진다.
> ForEach(0 ..< Define.ListTotal, **id: \.self**) { indexInt in
