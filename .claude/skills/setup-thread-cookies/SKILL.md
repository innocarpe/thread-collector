---
name: setup-thread-cookies
version: 1.0.0
description: |
  Threads.net 수집에 필요한 Chrome 쿠키 환경을 한 번에 셋업.
  pycookiecheat 설치 → Chrome 로그인 확인 → 쿠키 주입 테스트까지 one-stop.
  Usage: /setup-thread-cookies
allowed-tools:
  - Bash
  - AskUserQuestion
---

# /setup-thread-cookies

새 맥에서 `/collect` 를 쓰기 전에 딱 한 번 실행하면 됨.
pycookiecheat 설치 → Chrome 쿠키 확인 → browse 주입 테스트까지 자동 처리.

---

## Step 1: pycookiecheat 설치 확인

```bash
python3 -c "import pycookiecheat; print('OK')" 2>&1
```

출력이 `OK` 면 Step 2로. 아니면 설치:

```bash
pip3 install pycookiecheat 2>&1
```

실패 시 사용자에게 에러 메시지 전달하고 중단.

---

## Step 2: Chrome 쿠키에서 Threads 세션 확인

```bash
python3 - <<'EOF'
import os, sys
try:
    import pycookiecheat
except ImportError:
    print("ERROR: pycookiecheat 없음")
    sys.exit(1)

PROFILE_PATHS = [
    "~/Library/Application Support/Google/Chrome/Profile 7/Cookies",
    "~/Library/Application Support/Google/Chrome/Default/Cookies",
    "~/Library/Application Support/Chromium/Default/Cookies",
    "~/.config/google-chrome/Default/Cookies",
]

found = None
for p in PROFILE_PATHS:
    expanded = os.path.expanduser(p)
    if os.path.isfile(expanded):
        found = expanded
        break

if not found:
    print("ERROR: Chrome 프로필을 찾을 수 없음")
    sys.exit(1)

try:
    cookies = pycookiecheat.chrome_cookies("https://threads.com", cookie_file=found)
except Exception as e:
    print(f"ERROR: 쿠키 추출 실패 — {e}")
    sys.exit(1)

has_session = "sessionid" in cookies
print(f"PROFILE: {found}")
print(f"COOKIES: {list(cookies.keys())}")
print(f"SESSION: {'OK' if has_session else 'MISSING'}")
EOF
```

- `SESSION: OK` → Step 3으로
- `SESSION: MISSING` → 사용자에게 안내:
  > Chrome에서 https://www.threads.net 에 접속해 로그인해 주세요.
  > 로그인 완료 후 다시 `/setup-thread-cookies` 를 실행하세요.
  중단.
- `ERROR:` → 에러 메시지 전달하고 중단.

---

## Step 3: browse 바이너리 확인

```bash
python3 - <<'EOF'
import os, subprocess

BROWSE_BIN = os.path.expanduser("~/.claude/skills/gstack/browse/dist/browse")
BUN_EXEC   = os.path.expanduser("~/.bun/bin/bun")
CLI_TS     = os.path.expanduser("~/.claude/skills/gstack/browse/src/cli.ts")

# 컴파일 바이너리 확인
if os.path.isfile(BROWSE_BIN):
    r = subprocess.run([BROWSE_BIN, "--help"], capture_output=True, timeout=5)
    if r.returncode not in (137, -9):
        print("BROWSE: compiled binary OK")
    else:
        print("BROWSE: compiled binary killed by macOS (SIGKILL)")
        if os.path.isfile(BUN_EXEC) and os.path.isfile(CLI_TS):
            print("BROWSE: bun fallback available OK")
        else:
            print("ERROR: bun fallback 없음 — bun 설치 필요")
else:
    print("ERROR: browse 바이너리 없음 — gstack 설치 필요")
EOF
```

- `ERROR:` 포함 시 사용자에게 전달하고 중단.

---

## Step 4: 쿠키 주입 실제 테스트

```bash
python3 /Users/WooseongKim/Projects/Temperstone/thread-collector/scripts/setup_cookies.py 2>&1
```

`scripts/setup_cookies.py` 실행:

```bash
python3 - <<'EOF'
import os, sys, subprocess

sys.path.insert(0, "/Users/WooseongKim/Projects/Temperstone/thread-collector/scripts")

try:
    import pycookiecheat
except ImportError:
    print("ERROR: pycookiecheat 없음")
    sys.exit(1)

BROWSE_BIN = os.path.expanduser("~/.claude/skills/gstack/browse/dist/browse")
BUN_EXEC   = os.path.expanduser("~/.bun/bin/bun")
CLI_TS     = os.path.expanduser("~/.claude/skills/gstack/browse/src/cli.ts")

# browse 명령 결정
if os.path.isfile(BROWSE_BIN):
    r = subprocess.run([BROWSE_BIN, "--help"], capture_output=True, timeout=5)
    browse_cmd = [BROWSE_BIN] if r.returncode not in (137, -9) else [BUN_EXEC, "run", CLI_TS]
else:
    browse_cmd = [BUN_EXEC, "run", CLI_TS]

PROFILE_PATHS = [
    "~/Library/Application Support/Google/Chrome/Profile 7/Cookies",
    "~/Library/Application Support/Google/Chrome/Default/Cookies",
    "~/Library/Application Support/Chromium/Default/Cookies",
    "~/.config/google-chrome/Default/Cookies",
]
cookie_file = next(
    (os.path.expanduser(p) for p in PROFILE_PATHS if os.path.isfile(os.path.expanduser(p))),
    None
)
if not cookie_file:
    print("ERROR: Chrome 프로필 없음")
    sys.exit(1)

cookies = pycookiecheat.chrome_cookies("https://threads.com", cookie_file=cookie_file)
if "sessionid" not in cookies:
    print("ERROR: Threads 세션 없음 — Chrome에서 로그인 필요")
    sys.exit(1)

# threads.net으로 이동 후 쿠키 주입
subprocess.run(browse_cmd + ["goto", "https://www.threads.net"], capture_output=True, timeout=30)
injected = 0
for name, value in cookies.items():
    r = subprocess.run(browse_cmd + ["cookie", f"{name}={value}"], capture_output=True, timeout=10)
    if r.returncode == 0:
        injected += 1

print(f"SUCCESS: {injected}/{len(cookies)} 쿠키 주입 완료")
EOF
```

- `SUCCESS:` → Step 5로
- `ERROR:` → 에러 메시지 전달하고 중단

---

## Step 5: 완료 안내

아래를 사용자에게 출력:

```
✅ Threads 쿠키 셋업 완료

  - pycookiecheat: 설치됨
  - Chrome 세션: threads.net 로그인 확인
  - browse 쿠키 주입: 성공

이제 /collect @username 을 바로 실행할 수 있습니다.
```
