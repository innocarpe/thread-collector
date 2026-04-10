# ThreadCollector

Threads.net 유저의 게시글을 수집해서 인사이트를 카테고리별 마크다운으로 저장하는 도구.

## 프로젝트 구조

```
ThreadCollector/
├── .claude/skills/collect/SKILL.md   # /collect 스킬
├── scripts/fetch_threads.py          # Threads API 기반 수집기 (선택)
├── Threads/                          # 수집 결과 저장 디렉토리
│   └── {username}/
│       ├── tech-dev.md
│       ├── product-business.md
│       └── career-philosophy.md
└── .thread-collector-config          # API 키 (gitignore됨)
```

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.

Key routing rules:
- "/collect", "collect @username", "수집해", "게시글 모아줘", "threads 분석" → invoke `collect` skill
- 특정 유저 인사이트 요청, "@username 글 뽑아줘" → invoke `collect` skill
- "/run-blog", "블로그 켜줘", "로컬 실행", "dev 서버" → invoke `run-blog` skill
- "/setup-thread-cookies", "쿠키 셋업", "threads 로그인 설정", "새 맥 셋업" → invoke `setup-thread-cookies` skill

## 인사이트 카테고리

기본 분류 체계 (변경 시 SKILL.md도 함께 수정):

| 파일 | 내용 |
|------|------|
| `tech-dev.md` | 기술/개발: 코딩, 아키텍처, 툴, AI, 시스템 설계 |
| `product-business.md` | 프로덕트/비즈니스: PMF, 스타트업, 성장 전략 |
| `career-philosophy.md` | 커리어/철학: 일하는 방식, 마인드셋, 인생관 |

## 사용법

```
/collect @username                          # 기본 (전체 카테고리)
/collect @username --types tech,product     # 특정 카테고리만
/collect @username --limit 30               # 스크롤 횟수 제한
```

## API 설정 (선택사항)

browse 스크래핑 없이 공식 API 사용하려면:

1. [Meta Developer Console](https://developers.facebook.com/apps/) 에서 Threads 앱 생성
2. `.thread-collector-config` 파일 생성:
   ```
   ACCESS_TOKEN=your_token_here
   ```
3. 설정 확인: `python3 scripts/fetch_threads.py --check-config`
