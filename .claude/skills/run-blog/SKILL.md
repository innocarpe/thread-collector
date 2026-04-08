---
name: run-blog
version: 1.0.0
description: ThreadCollector 블로그를 백그라운드에서 실행하고 브라우저로 엽니다.
allowed-tools:
  - Bash
---

# /run-blog — ThreadCollector 로컬 실행

```bash
# 이미 실행 중이면 종료
pkill -f "next dev" 2>/dev/null || true
sleep 1

# 백그라운드로 dev 서버 실행
cd /Users/WooseongKim/Projects/TemperStone/ThreadCollector
npm run dev > /tmp/thread-collector-dev.log 2>&1 &
echo "PID: $!"

# 서버가 뜰 때까지 대기 (최대 10초)
for i in $(seq 1 20); do
  sleep 0.5
  PORT=$(grep -m1 "Local:" /tmp/thread-collector-dev.log 2>/dev/null | grep -oE ":[0-9]+" | tr -d ':')
  if [ -n "$PORT" ]; then
    echo "Running on http://localhost:$PORT"
    open "http://localhost:$PORT"
    break
  fi
done
```

로그는 `/tmp/thread-collector-dev.log` 에서 확인 가능.
종료하려면 `pkill -f "next dev"`.
