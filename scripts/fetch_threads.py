#!/usr/bin/env python3
"""
ThreadCollector - Threads API 기반 게시글 수집기 (선택사항)

browse 스크래핑 대신 공식 Threads API를 사용할 때 이 스크립트를 씁니다.
공식 Meta Threads API 문서: https://developers.facebook.com/docs/threads

설정:
  .thread-collector-config (프로젝트 루트) 또는 ~/.thread-collector-config 에:
  ACCESS_TOKEN=your_token_here
  USER_ID=your_user_id_here (본인 계정 ID, 다른 유저 조회시에도 필요)
"""

import sys
import json
import argparse
import os
import time
from pathlib import Path
from datetime import datetime


def load_config() -> dict:
    """설정 파일에서 API 토큰 로드."""
    config_paths = [
        Path(".thread-collector-config"),
        Path.home() / ".thread-collector-config",
    ]
    for path in config_paths:
        if path.exists():
            config = {}
            for line in path.read_text().strip().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    config[key.strip()] = value.strip()
            return config
    return {}


def check_config() -> bool:
    """API 설정이 완료되었는지 확인."""
    config = load_config()
    return bool(config.get("ACCESS_TOKEN"))


def fetch_user_id(username: str, access_token: str) -> str | None:
    """username으로 Threads user ID 조회."""
    import urllib.request
    import urllib.parse

    url = f"https://graph.threads.net/v1.0/users/{username}?fields=id,username&access_token={access_token}"
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read())
            return data.get("id")
    except Exception as e:
        print(f"ERROR: user ID 조회 실패: {e}", file=sys.stderr)
        return None


def fetch_posts(user_id: str, access_token: str, limit: int = 100) -> list[dict]:
    """
    Threads API로 유저 게시글 수집.
    페이지네이션 처리해서 가능한 모든 게시글 가져옴.
    """
    import urllib.request
    import urllib.parse

    all_posts = []
    url = (
        f"https://graph.threads.net/v1.0/{user_id}/threads"
        f"?fields=id,text,timestamp,media_type,is_reply"
        f"&limit=100"
        f"&access_token={access_token}"
    )

    page = 0
    while url and len(all_posts) < limit:
        page += 1
        print(f"  페이지 {page} 요청 중...", file=sys.stderr)

        try:
            with urllib.request.urlopen(url) as resp:
                data = json.loads(resp.read())
        except Exception as e:
            print(f"ERROR: API 요청 실패: {e}", file=sys.stderr)
            break

        posts = data.get("data", [])
        for post in posts:
            # 리플라이 제외, 텍스트 있는 원본 게시글만
            if post.get("is_reply"):
                continue
            text = post.get("text", "").strip()
            if not text or len(text) < 20:
                continue
            all_posts.append({
                "id": post.get("id"),
                "text": text,
                "timestamp": post.get("timestamp"),
                "media_type": post.get("media_type"),
            })

        # 다음 페이지 URL
        paging = data.get("paging", {})
        url = paging.get("next")

        # Rate limit 방지
        time.sleep(0.5)

    print(f"  총 {len(all_posts)}개 게시글 수집", file=sys.stderr)
    return all_posts


def main():
    parser = argparse.ArgumentParser(description="Threads 게시글 수집기")
    parser.add_argument("username", nargs="?", help="Threads 유저명 (@ 없이)")
    parser.add_argument("--output", "-o", help="JSON 출력 파일 경로")
    parser.add_argument("--limit", type=int, default=500, help="최대 게시글 수 (기본: 500)")
    parser.add_argument("--check-config", action="store_true", help="API 설정 확인")
    args = parser.parse_args()

    if args.check_config:
        if check_config():
            print("CONFIG_OK")
            sys.exit(0)
        else:
            print("CONFIG_MISSING", file=sys.stderr)
            print("", file=sys.stderr)
            print("설정 방법:", file=sys.stderr)
            print("  1. Meta Developer Console에서 Threads 앱 생성", file=sys.stderr)
            print("     https://developers.facebook.com/apps/", file=sys.stderr)
            print("  2. .thread-collector-config 파일에 아래 내용 추가:", file=sys.stderr)
            print("     ACCESS_TOKEN=your_access_token", file=sys.stderr)
            sys.exit(1)

    if not args.username:
        print("ERROR: username이 필요합니다", file=sys.stderr)
        sys.exit(1)

    username = args.username.lstrip("@")
    config = load_config()
    access_token = config.get("ACCESS_TOKEN")

    if not access_token:
        print("ERROR: ACCESS_TOKEN이 설정되지 않았습니다", file=sys.stderr)
        print("--check-config 로 설정 방법을 확인하세요", file=sys.stderr)
        sys.exit(1)

    print(f"@{username} 게시글 수집 중...", file=sys.stderr)

    # user ID 조회 (username이 숫자 ID가 아닌 경우)
    user_id = username
    if not username.isdigit():
        user_id = fetch_user_id(username, access_token)
        if not user_id:
            # 공개 API로 username 직접 조회 시도
            user_id = username  # fallback: username을 그대로 사용

    posts = fetch_posts(user_id, access_token, limit=args.limit)

    result = {
        "username": username,
        "fetched_at": datetime.now().isoformat(),
        "post_count": len(posts),
        "posts": posts,
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"저장 완료: {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
