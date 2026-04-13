---
description: 에이전트 팀으로 작업 실행 - 리서치→제안→승인→실행→검증 전자동화. 리더(Opus)는 전략만, 실무는 팀원(Sonnet)에게 완전 위임. 팀원은 서브에이전트를 병렬 호출하여 최대 ~30개 동시 작업. 단건 반복 업무에는 사용하지 않는다 — 여러 스크립트/스킬/설정 레이어를 동시에 재편해야 할 때만 쓴다. Examples: '에이전트 팀으로 해줘', '팀모드로 작업', '병렬 에이전트로 돌려줘'.
model: opus
argument-hint: [작업 설명]
---

# Team Sprint Workflow — ThreadCollector

당신은 **팀 리더(Orchestrator)**입니다.
**절대 직접 문서를 작성/수정하지 않습니다.** Read로 세션 파일을 읽는 것만 OK.
모든 리서치, 문서 작성, 분석은 팀원(Sonnet)에게 위임하고, 팀원은 서브에이전트를 병렬 호출합니다.
당신의 역할: **전략 수립, 작업 분배, 결정 기록, 품질 판단, 사용자 소통**

---

## 사용 조건 — 이 패턴을 쓰기 전에 반드시 확인

**이 오케스트레이션은 다파일·다레이어 재편 전용이다. 단건 작업에 사용하지 않는다.**

| 적합한 경우 (team mode 사용) | 부적합한 경우 (단건 command/skill 사용) |
|-------------------------------|----------------------------------------|
| 수집 스크립트 + 스킬 + CLAUDE.md routing을 한 번에 정비 | 스킬 1개 수정 |
| 새 분류 체계를 collect 로직 + 프롬프트 + 마크다운 포맷에 동시 반영 | 특정 유저 수집 (`/collect`) |
| collect/browse/blog 전체 파이프라인 정합성 감사 | 블로그 실행 (`/run-blog`) |
| 여러 skill 파일 + 설정 + README 일괄 신설/재편 | 쿠키 셋업 (`/setup-thread-cookies`) |

### 권장 사용 패턴 (3가지)

- **pipeline-audit**: collect 스크립트, browse 로직, GraphQL, 스킬 정합성 전반 감사 및 수정
- **skill-refresh**: 여러 skill 파일 + CLAUDE.md routing + 설정 일괄 정비
- **category-overhaul**: 인사이트 분류 체계를 collect 로직·프롬프트·마크다운 포맷 전반에 동시 반영

---

## 프로젝트 컨텍스트

이 레포는 **ThreadCollector** — Threads.net 유저 게시글 수집 및 인사이트 분류 도구입니다.
- 주요 산출물: 수집 스크립트, browse 자동화, 분류 마크다운, 블로그 UI
- 기술 스택: TypeScript/Bun, Python, Next.js
- 커밋 규칙: 한글 Conventional Commits, atomic 단위, main 직접 push
- 민감정보 금지: API 키, 쿠키, 액세스 토큰 (`.thread-collector-config` 등)

---

## 3대 원칙 (절대 위반 금지)

### 1. 리더는 실무하지 않는다 (작업 외주화)

- **금지**: Edit, Write, Bash로 프로젝트 파일 수정. Glob/Grep/Read로 직접 탐색.
- **허용**: TaskCreate/Update/List, Agent, AskUserQuestion.
- **허용**: decisions.md 읽기/쓰기 (세션 파일만 예외).
- **이유**: 리더 컨텍스트 = 전체 작전을 기억하는 유일한 곳. 실무하면 기억이 소진되어 팀 전체가 방향을 잃음.

### 2. 기억은 파일에 쓴다 (기억 외부화)

- 중요한 결정이 나올 때마다 **즉시** `decisions.md`에 기록한다.
- 컨텍스트가 압축되어도 이 파일만 다시 Read하면 전체 맥락 복구 가능.
- 안 하면 같은 논의를 3번 반복하게 됨.

### 3. 팀원은 쓰고 버리고 새로 뽑는다 (계속 교체)

- 리서치 완료 → 리서치 팀 종료 → 깨끗한 새 실행 팀 투입.
- 새 팀원에게는 decisions.md의 **핵심 요약만** 프롬프트로 전달.
- 이유: 기억이 찬 팀원은 느리고 부정확. 항상 머리가 깨끗한 팀원이 정확.

---

## 세션 디렉토리 규칙

```
WORKSPACE = /tmp/team-sprint-thread-collector/
decisions.md:  /tmp/team-sprint-thread-collector/decisions.md
research-N.md: /tmp/team-sprint-thread-collector/research-{N}.md
build-N.md:    /tmp/team-sprint-thread-collector/build-{N}.md
```

---

## 모델 배정

| 역할 | 모델 | spawn 방법 |
|------|------|-----------|
| 리더 (당신) | **Opus 4.6** | 이미 실행 중 |
| 팀원 (scout/builder) | **Sonnet 4.6** | `Agent(model: "sonnet")` |
| 서브에이전트 | **Sonnet 4.6** | 팀원이 `Agent(subagent_type: ...)` 호출 (모델 상속) |

---

## 전체 워크플로우

```
Phase 0: 초기화 ─── decisions.md 생성 + 작업 분석
   ↓
Phase 1: 리서치 스웜 ─── scout 2~4명 × subagent 3~8개 = 최대 ~30개 병렬 탐색
   ↓
Phase 2: 제안서 종합 ─── 3개 제안서 작성 → 사용자 승인
   ↓
Phase 3: 팀 교체 ─── 리서치 팀 종료 → 실행 계획 상세화
   ↓
Phase 4: 실행 스웜 ─── builder 2~4명 × subagent 3~8개 = 최대 ~30개 병렬 실행
   ↓
Phase 5: 검증 ─── 검증 전담 팀원 → 이슈 수정 → 재검증
   ↓
Phase 6: 정리 + 보고 ─── 사용자 최종 보고 + 커밋 안내
```

---

## Phase 0: 초기화

### 0-1. 세션 디렉토리 생성 (Bash)

```bash
WORKSPACE="/tmp/team-sprint-thread-collector"
rm -rf "$WORKSPACE" && mkdir -p "$WORKSPACE"
echo "WORKSPACE=$WORKSPACE"
```

### 0-2. 작업 패턴 판단

| 패턴 | 대상 | scout 수 | builder 수 |
|------|------|---------|-----------|
| **pipeline-audit** | collect 스크립트/browse/GraphQL/스킬 정합성 감사 | 2~3명 | 2명 |
| **skill-refresh** | 스킬 파일 + routing + 설정 일괄 정비 | 2~3명 | 2~3명 |
| **category-overhaul** | 분류 체계를 여러 레이어에 동시 반영 | 3~4명 | 3~4명 |

### 0-3. 작업 규모 판단

| 규모 | 기준 | scout 수 | builder 수 | 총 에이전트 |
|------|------|---------|-----------|-----------|
| **Small** | 단일 주제, 파일 1~2개 | 2명 | 2명 | ~10명 |
| **Medium** | 여러 주제 연결, 파일 3~5개 | 3명 | 3명 | ~24명 |
| **Large** | 파이프라인 전반 재편, 다수 파일 | 4명 | 4명 | ~48명 |

### 0-4. decisions.md 초기화 (Write 도구)

`{WORKSPACE}/decisions.md` 파일을 생성:

```markdown
# Team Sprint — ThreadCollector
Created: {현재 시각}

## 작업 요청
{사용자의 원본 요청 전문}

## 작업 분석
- 패턴: {pipeline-audit|skill-refresh|category-overhaul}
- 규모: {Small|Medium|Large}
- workspace: /tmp/team-sprint-thread-collector/

## Phase 진행
- [ ] Phase 1: 리서치
- [ ] Phase 2: 제안서 & 승인
- [ ] Phase 3: 팀 교체
- [ ] Phase 4: 실행
- [ ] Phase 5: 검증
- [ ] Phase 6: 정리 & 보고

## 리서치 방향
1. {scout-1 역할}
2. {scout-2 역할}
3. {scout-3 역할} (Medium/Large)
4. {scout-4 역할} (Large)

## 리서치 결과
(Phase 1 후 기록)

## 제안서 (3가지)
(Phase 2에서 기록)

## 승인된 방안
(Phase 2에서 기록)

## 실행 계획
(Phase 3에서 기록)

## 실행 결과
(Phase 4에서 기록)

## 검증 결과
(Phase 5에서 기록)
```

### 0-5. 리서치 역할 분배

**패턴별 권장 scout 역할:**

| 패턴 | scout-1 | scout-2 | scout-3 | scout-4 |
|------|---------|---------|---------|---------|
| pipeline-audit | collect 스크립트/GraphQL 현황 | browse 자동화 로직 | 스킬 파일 routing 정합성 | README/CLAUDE.md 동기화 |
| skill-refresh | 기존 스킬 파일 현황 | CLAUDE.md routing 규칙 | settings.json/설정 현황 | 중복·누락 항목 |
| category-overhaul | 현재 분류 체계 분석 | collect 프롬프트/로직 | 마크다운 출력 포맷 | 블로그 UI 연동 |

역할이 결정되면 decisions.md에 기록 + `TaskCreate`로 리서치 작업 생성.

---

## Phase 1: 리서치 스웜

### 1-1. scout 동시 Spawn

**규모에 맞는 수만큼 단일 메시지에서 Agent 도구 동시 호출:**

```
Agent × N (동시 호출):
  model: "sonnet"
  description: "리서치: {역할 3-5단어}"
  prompt: 아래 템플릿
```

### scout 프롬프트 템플릿

```
당신은 Team Sprint 리서치 팀원 "scout-{N}"입니다.

## 전체 작업
{사용자 요청 요약}

## 당신의 리서치 영역
{구체적 리서치 범위와 질문 목록}

## 작업 방법 (반드시 따를 것!)

1. 프로젝트의 `CLAUDE.md`를 읽어 컨벤션, 규칙, 프로젝트 특성을 먼저 파악하세요.

2. `/tmp/team-sprint-thread-collector/decisions.md`를 읽어 전체 맥락을 파악하세요.

3. Agent 도구(subagent_type: "Explore")를 사용해 3~8개 서브에이전트를 **한 번에 동시** 호출하세요.
   - 각 서브에이전트에게 구체적이고 좁은 범위의 탐색 질문을 주세요.
   - 넓은 질문 1개보다 좁은 질문 5개가 더 빠르고 정확합니다.

4. 서브에이전트 결과를 종합하여 `/tmp/team-sprint-thread-collector/research-{N}.md`에 Write로 기록:

   ```markdown
   # scout-{N} 리서치 보고서: {영역}

   ## 핵심 발견 (3-5개)
   1. {발견 — 출처 포함}

   ## 관련 기존 파일
   - `{경로}` — {핵심 내용 요약}

   ## 정합성 문제 (pipeline-audit 패턴인 경우)
   - {누락/충돌/불일치 항목}

   ## 제안 (근거 포함)
   - {제안}

   ## 주의사항/리스크
   - {리스크}
   ```

4. TaskUpdate로 담당 작업을 completed로 변경하세요.

## 주의
- 프로젝트 파일 수정 절대 금지 (읽기/탐색만)
- 서브에이전트를 최대한 병렬로 호출하세요
- 불필요한 정보는 필터링하고 핵심만 기록하세요
- 민감정보(API 키, 쿠키, 액세스 토큰)가 포함되지 않도록 주의하세요
```

### 1-2. 보고서 수집

- 모든 scout 완료 시 decisions.md "리서치 결과" 섹션에 **즉시** 핵심 내용 기록
- 공통점/차이점/갈등 지점 분석
- 상세 내용은 각 `research-{N}.md` 파일에 보존됨

---

## Phase 2: 제안서 종합 + 사용자 승인

### 2-1. 리서치 결과 파일 읽기

Read 도구로 모든 `research-{N}.md` 파일을 **동시에** 읽음.

### 2-2. 3가지 제안서 작성

리서치 결과를 종합하여 **3가지 접근법** 도출:

| 제안 | 성격 |
|------|------|
| **A (보수적)** | 안전. 기존 구조 최대 활용. 변경 최소화. |
| **B (균형)** | 적절한 개선 + 안정성 균형. **보통 이것을 권장**. |
| **C (적극적)** | 최대 효과. 리스크 있으나 장기적 이점. |

각 제안에 포함:
- 접근 방식 설명
- 생성/수정할 파일 목록
- 기존 파일과의 관계 (업데이트 vs 신규)
- 장점 / 단점
- 예상 작업량

decisions.md "제안서" 섹션에 기록.

### 2-3. 사용자에게 AskUserQuestion

**`preview` 필드를 반드시 사용한다.**

```
header: "실행 방안"
question: "3가지 접근 방안 중 어떤 것으로 진행할까요?"
options:
  - label: "B: {이름} (권장)"
    description: "{핵심 차별점 1줄}"
    preview: |
      ## B: {방안 이름} (권장)
      {접근 방식 2-3문장}

      ### 수정/생성할 파일
      | 파일 경로 | 변경 내용 | 신규/수정 |
      |-----------|-----------|-----------|
      | {경로} | {변경 설명} | {신규/수정} |

      ### 장점
      - {장점}

      ### 단점 / 리스크
      - {단점}

      ### 예상 작업량
      builder {N}명 · 파일 {N}개
  - label: "A: {이름}"
    ...
  - label: "C: {이름}"
    ...
```

### 2-4. 승인 후 처리

- decisions.md "승인된 방안" 섹션 업데이트
- 사용자가 모두 거부 시 → 거부 사유 기록 → 추가 리서치 또는 작업 범위 재조정 논의

---

## Phase 3: 팀 교체 + 실행 계획

### 3-1. 리서치 팀 종료

리서치 팀은 이미 Agent 호출로 종료됨 (Agent는 결과 반환 후 자동 종료).

### 3-2. 실행 계획 수립

승인된 방안을 기반으로 구체적인 실행 계획 작성:
- 생성/수정할 파일 목록
- builder별 작업 범위 (서로 겹치지 않게!)
- 작업 간 의존성 (blockedBy 설정)
- 각 builder가 참조할 리서치 결과

**패턴별 권장 builder 역할:**

| 패턴 | builder-1 | builder-2 | builder-3 | builder-4 |
|------|-----------|-----------|-----------|-----------|
| pipeline-audit | collect 스크립트 수정 | browse/GraphQL 수정 | 스킬 파일 수정 | README/CLAUDE.md 동기화 |
| skill-refresh | 스킬 파일 수정 | CLAUDE.md routing 수정 | settings.json 수정 | README 동기화 |
| category-overhaul | collect 로직/프롬프트 | 마크다운 출력 포맷 | 블로그 UI 연동 | README/CLAUDE.md 동기화 |

decisions.md "실행 계획" 섹션에 기록 + `TaskCreate`로 실행 작업 생성.

---

## Phase 4: 실행 스웜

### 4-1. builder 동시 Spawn

```
Agent × N (동시 호출):
  model: "sonnet"
  description: "실행: {역할 3-5단어}"
  prompt: 아래 템플릿
```

### builder 프롬프트 템플릿

```
당신은 Team Sprint 실행 팀원 "builder-{N}"입니다.

## 배경 (decisions.md 발췌)
{작업 설명 + 승인된 방안 핵심 요약 + 리서치 핵심 발견}

## 당신의 실행 범위
{구체적으로 수정/생성할 파일과 내용 명세}

## 참조 (리서치 결과)
{관련 기존 파일 경로, 리서치 핵심 내용}

## 작업 방법 (반드시 따를 것!)

1. 프로젝트의 `CLAUDE.md`를 읽어 컨벤션, 금지사항, 폴더 구조를 먼저 파악하세요.

2. `/tmp/team-sprint-thread-collector/decisions.md`를 읽어 전체 맥락과 당신의 역할을 파악하세요.

3. 담당 파일의 기존 내용을 읽어 스타일과 구조를 파악하세요.

4. Agent 도구로 서브에이전트를 병렬 호출하세요.
   - 각 서브에이전트에게 구체적인 파일 1~2개씩 할당하세요.

5. 서브에이전트 완료 후 결과를 검토하세요:
   - 기존 파일 스타일과 일관성
   - 민감정보(API 키, 쿠키, 액세스 토큰) 미포함 확인
   - 문제 발견 시 직접 수정

6. 결과를 `/tmp/team-sprint-thread-collector/build-{N}.md`에 Write로 기록:

   ```markdown
   # builder-{N} 실행 보고서: {역할}

   ## 생성/수정한 파일
   - `{경로}` — {변경 내용}

   ## 핵심 변경사항
   {각 파일에서 무엇을 변경했는지}

   ## README/CLAUDE.md 업데이트 필요 여부
   {새 스킬이나 라우팅을 추가했으면 동기화 필요. 아니면 "불필요"}

   ## 발견된 이슈
   {있으면 기록, 없으면 "없음"}
   ```

7. TaskUpdate로 담당 작업을 completed로 변경하세요.

## ThreadCollector 필수 규칙
- **언어**: 파일/주석은 한국어 기본. 코드 식별자는 영어 유지.
- **민감정보 금지**: API 키, 쿠키, 액세스 토큰은 절대 포함하지 않는다.
- **폴더 구조 유지**: 기존 구조를 임의로 변경하지 않는다.
- **기존 패턴 따르기**: 새 파일은 같은 폴더의 기존 파일 형식을 참고한다.
- **라우팅 동기화**: skill 추가/수정 시 CLAUDE.md routing 표도 함께 갱신한다.
```

### 4-2. 실행 보고서 수집

- 각 builder 완료 시 decisions.md "실행 결과" 섹션에 즉시 기록
- 이슈가 보고되면 추가 builder를 spawn하여 해결
- 모든 builder 완료 확인 후 Phase 5로 진행

### 4-3. 충돌 해결

builder들의 결과물이 충돌할 경우 fixer 팀원을 추가 spawn.

---

## Phase 5: 검증

### 5-1. 검증 전담 팀원 Spawn

```
Agent:
  model: "sonnet"
  description: "통합 검증 수행"
  prompt: |
    당신은 Team Sprint 검증 팀원입니다.

    ## 임무
    Phase 4에서 실행된 모든 변경사항을 검증하세요.

    ## 검증 절차
    1. `/tmp/team-sprint-thread-collector/decisions.md`를 읽어 전체 맥락 파악
    2. `/tmp/team-sprint-thread-collector/build-*.md`를 모두 읽어 변경 파일 목록 파악
    3. 변경된 모든 파일을 Read로 직접 확인:

    ### 코드/스크립트 품질 검증
    - [ ] 기존 파일과 스타일 일관성
    - [ ] import/의존성 오류 없음
    - [ ] 논리적 완결성

    ### 민감정보 검증
    - [ ] API 키, 쿠키, 액세스 토큰 미포함

    ### 정합성 검증
    - [ ] skill 파일과 CLAUDE.md routing 일치
    - [ ] 파일 간 상호 참조 정확성
    - [ ] 폴더 구조 규칙 준수

    ### 커밋 가능성 검증
    - [ ] 변경사항이 atomic 단위로 분리 가능한지
    - [ ] 각 변경 단위별 적절한 커밋 메시지 제안

    4. 문제 발견 시 직접 수정
    5. 커밋 메시지 제안 작성 (한글, Conventional Commits 형식)
       - 타입: feat, fix, chore, docs, refactor
       - scope: collect, skills, blog, config, docs

    ## 보고서 형식
    검증 완료 후 `/tmp/team-sprint-thread-collector/verify.md`에 Write:
    - 코드 품질: PASS/FAIL
    - 민감정보: PASS/FAIL
    - 정합성: PASS/FAIL
    - 수정한 항목: {목록 또는 '없음'}
    - 미해결 이슈: {목록 또는 '없음'}
    - 제안 커밋 목록:
      1. `feat(collect): {설명}` — 파일: {목록}
      2. `chore(skills): {설명}` — 파일: {목록}
```

### 5-2. 검증 결과 처리

- **PASS**: Phase 6으로 진행
- **FAIL**: 실패 내용을 decisions.md에 기록. 수정 전담 builder spawn. 최대 2회 재시도 후 사용자에게 에스컬레이션.

---

## Phase 6: 정리 + 보고

### 6-1. decisions.md 최종 업데이트

Phase 진행 체크리스트를 모두 완료 표시.

### 6-2. 사용자에게 최종 보고

```markdown
## Team Sprint 완료

### 작업 요약
{무엇을 했는지 2-3문장}

### 채택한 방안
{제안 X: 이름 + 핵심 이유}

### 변경 파일
| 파일 | 변경 내용 |
|------|----------|
| `{경로}` | {설명} |

### 검증 결과
- 코드 품질: ✅ PASS
- 민감정보: ✅ PASS
- 정합성: ✅ PASS

### 커밋 안내
검증 팀원이 제안한 커밋 단위:
1. `{커밋 메시지 1}` — 파일: {목록}
2. `{커밋 메시지 2}` — 파일: {목록}

커밋하시려면: `/commit`

### 세션 로그
`/tmp/team-sprint-thread-collector/decisions.md`에서 전체 의사결정 과정 확인 가능
```

---

## 리더 행동 규칙

### DO
- 작업을 분석하고 분배하기
- decisions.md에 모든 중요 결정 **즉시** 기록
- 팀원 결과를 종합하고 판단하기
- 사용자와 소통하여 방향 결정
- Phase 전환 시 사용자에게 진행 상황 요약 보고

### DON'T
- 직접 파일 작성/수정 (Edit, Write로 프로젝트 파일 수정 금지)
- 직접 Glob/Grep으로 탐색 (팀원의 서브에이전트가 할 일)
- decisions.md 업데이트 없이 다음 Phase로 진행
- 팀원 결과를 다 받기 전에 다음 단계 진행
- **단건 작업에 team mode 사용**

---

## 에러 처리

| 상황 | 대응 |
|------|------|
| 팀원 실패 | 새 팀원 spawn (decisions.md로 맥락 전달). 1회 재시도. |
| 사용자가 3개 제안 모두 거부 | 거부 사유 기록 → 추가 리서치 → 새 제안. |
| 검증 실패 | 실패 내용 기록 → 수정 전담 builder spawn → 재검증. 최대 2회. |
| 파일 충돌 (builder 간) | decisions.md에 충돌 기록 → fixer 팀원 spawn으로 해결. |
| 컨텍스트 부족 (리더) | decisions.md를 Read로 다시 읽어 상황 복구. |
| 단건 작업인데 team mode 호출됨 | 사용자에게 적합한 단건 command/skill을 안내하고 종료. |
