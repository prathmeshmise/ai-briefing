#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# publish.sh — publish the AI briefing to GitHub Pages and post it to Slack.
#
# Run this on your Mac (NOT inside Cowork) a few minutes after the Cowork
# scheduled task has written briefings-data.js / briefings.json.
# A launchd job (see com.aibriefing.publish.plist) runs it daily at 19:15.
#
# One-time setup:
#   1. Fill in PAGES_URL below.
#   2. Put your Slack Incoming Webhook URL in a file next to this script named
#      ".slack_webhook"  (it is gitignored so it never gets committed):
#         echo 'https://hooks.slack.com/services/XXX/YYY/ZZZ' > .slack_webhook
#      (Alternatively export SLACK_WEBHOOK_URL in the environment.)
#   3. chmod +x publish.sh
# ---------------------------------------------------------------------------
set -euo pipefail

REPO_DIR="$HOME/Documents/Claude/AI-Briefing"
PAGES_URL="https://YOUR_GITHUB_USERNAME.github.io/ai-briefing/"   # <-- EDIT

cd "$REPO_DIR"

# --- resolve Slack webhook (file takes precedence over env) ---
if [[ -f ".slack_webhook" ]]; then
  SLACK_WEBHOOK_URL="$(tr -d '[:space:]' < .slack_webhook)"
fi
SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"

# --- 1) publish to GitHub Pages (only if something changed) ---
git add -A
if git diff --cached --quiet; then
  echo "$(date '+%F %T') no changes to publish"
else
  git commit -m "Briefing $(TZ=Asia/Kolkata date +%F)" >/dev/null
  git push origin main
  echo "$(date '+%F %T') pushed to GitHub Pages"
fi

# --- 2) build the Slack message from today's top-of-mind line ---
PAYLOAD="$(PAGES_URL="$PAGES_URL" python3 - <<'PY'
import json, os, re, pathlib, datetime
try:
    data = json.loads(pathlib.Path("briefings.json").read_text() or "[]")
except Exception:
    data = []
topline = ""
if data:
    md = data[0].get("markdown", "")
    m = re.search(r"\*\*Top of mind:\*\*\s*(.+)", md)
    if m:
        # drop markdown links, keep the visible text
        topline = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1", m.group(1)).strip()
ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
date = datetime.datetime.now(ist).strftime("%A, %d %b %Y")
url = os.environ["PAGES_URL"]
text = f"*AI Data Intelligence — {date}*\n{topline}\n\n:newspaper: <{url}|Read the full briefing>"
print(json.dumps({"text": text}))
PY
)"

# --- 3) post to Slack ---
if [[ -z "$SLACK_WEBHOOK_URL" ]]; then
  echo "$(date '+%F %T') SLACK_WEBHOOK_URL not set — skipping Slack post" >&2
else
  curl -sS -X POST -H 'Content-type: application/json' --data "$PAYLOAD" "$SLACK_WEBHOOK_URL" >/dev/null
  echo "$(date '+%F %T') posted to Slack"
fi
