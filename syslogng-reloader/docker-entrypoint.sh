#!/usr/bin/env bash
set -Eeuo pipefail

# ---- Tunables ----
CONF_DIR="${CONF_DIR:-/etc/syslog-ng}"
CONF_FILE="${CONF_FILE:-/etc/syslog-ng/syslog-ng.conf}"
CONTROL_SOCK="${CONTROL_SOCK:-/run/syslog-ng.ctl}"

# Inotify tuning: include more events (atomic saves often = moved_to)
INOTIFY_EVENTS="${INOTIFY_EVENTS:-close_write,modify,attrib,move,create,delete,moved_to,moved_from}"
DEBOUNCE_MS="${DEBOUNCE_MS:-500}"

# Polling fallback (helps on Docker Desktop/macOS/Windows bind mounts)
POLL_ENABLED="${POLL_ENABLED:-1}"       # 0=off, 1=on
POLL_INTERVAL_SEC="${POLL_INTERVAL_SEC:-5}"

# Resolve binaries (portable across image variants)
SYSLOGD="$(command -v syslog-ng || echo /usr/sbin/syslog-ng)"
CTL="$(command -v syslog-ng-ctl || echo /usr/sbin/syslog-ng-ctl)"

# ---- Start syslog-ng ----
"$SYSLOGD" --control="${CONTROL_SOCK}" \
           -f "${CONF_FILE}" \
           -F \
           --no-caps &
SYSLOG_PID=$!

cleanup() { kill -TERM "${SYSLOG_PID}" 2>/dev/null || true; wait "${SYSLOG_PID}" || true; }
trap cleanup SIGINT SIGTERM EXIT

# Track last reload time (ms since epoch) to let the poller skip duplicates
LAST_RELOAD_MS=0

reload_syslog() {
  # Include --no-caps in the syntax check to avoid capability warnings
  if "$SYSLOGD" --no-caps -s -f "${CONF_FILE}" 2>/dev/null; then
    if "$CTL" --control="${CONTROL_SOCK}" reload; then
      echo "[reloader] graceful reload via syslog-ng-ctl @ $(date '+%F %T')"
    else
      kill -HUP "${SYSLOG_PID}" && echo "[reloader] graceful reload via SIGHUP @ $(date '+%F %T')"
    fi
    LAST_RELOAD_MS=$(date +%s%3N)
  else
    echo "[reloader] syntax error; NOT reloading" >&2
  fi
}

# Wait briefly for the control socket to appear
for _ in $(seq 1 50); do
  [ -S "${CONTROL_SOCK}" ] && break
  sleep 0.1
done

# ---- Inotify watcher (with debounce + verbose) ----
(
  LAST_TS=0
  inotifywait -mqre "${INOTIFY_EVENTS}" --format '%e %w%f' "${CONF_DIR}" 2>/dev/null | \
  while read -r EVENT FILE; do
    NOW_MS=$(($(date +%s%3N)))
    if (( NOW_MS - LAST_TS < DEBOUNCE_MS )); then
      LAST_TS=${NOW_MS}
      continue
    fi
    LAST_TS=${NOW_MS}
    echo "[reloader] change detected: event='${EVENT}' file='${FILE}'"
    sleep 0.2
    reload_syslog
  done
) &

# ---- Polling fallback (portable) ----
hash_tree() {
  # Print "path mtime size" for every file, sort it, then hash the list.
  if stat -c %n /dev/null >/dev/null 2>&1; then
    # GNU/BusyBox stat
    find "${CONF_DIR}" -type f -exec stat -c '%n %Y %s' {} + 2>/dev/null \
      | sort \
      | sha1sum \
      | awk '{print $1}'
  else
    # BSD stat (unlikely inside Linux containers, but safe fallback)
    find "${CONF_DIR}" -type f -exec stat -f '%N %m %z' {} + 2>/dev/null \
      | sort \
      | shasum -a 1 \
      | awk '{print $1}'
  fi
}

if [ "${POLL_ENABLED:-1}" = "1" ]; then
  (
    LAST_HASH="$(hash_tree || true)"
    while sleep "${POLL_INTERVAL_SEC:-5}"; do
      CUR_HASH="$(hash_tree || true)"
      if [ "${CUR_HASH}" != "${LAST_HASH}" ]; then
        NOW_MS=$(date +%s%3N)
        # Skip if we reloaded very recently via inotify (1s window)
        if [ $((NOW_MS - LAST_RELOAD_MS)) -lt 1000 ]; then
          LAST_HASH="${CUR_HASH}"
          continue
        fi
        echo "[reloader] polling detected change in ${CONF_DIR}"
        LAST_HASH="${CUR_HASH}"
        reload_syslog
      fi
    done
  ) &
fi

# ---- Wait on syslog-ng ----
wait "${SYSLOG_PID}"