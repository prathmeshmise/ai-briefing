# AI Data Intelligence — Daily Briefing (hosting + Slack)

This folder is a self-contained static site. `index.html` (and `viewer.html`) read
`briefings-data.js`, which your Cowork scheduled task rewrites every evening.
Hosting it just means serving these files; sharing it means posting a link to Slack
each day.

## Architecture (why it's split this way)

- **Cowork scheduled task** — generates the briefing and writes `briefings.json` +
  `briefings-data.js` locally at ~19:01 IST. It runs in a sandbox that cannot use
  `git` on this folder or reach GitHub/Slack over the network, so it does **not**
  publish.
- **Your Mac (`publish.sh` via launchd)** — at 19:15 IST pushes the updated files to
  GitHub (which auto-deploys GitHub Pages) and posts the day's headline + link to
  Slack via an Incoming Webhook. `git` and `curl` work normally here.

## One-time setup

### 0. Clean up the half-initialised git folder
An earlier automated attempt left a broken `.git` here. In Terminal:
```bash
cd ~/Documents/Claude/AI-Briefing
rm -rf .git
```

### 1. Create the GitHub repo and push
```bash
cd ~/Documents/Claude/AI-Briefing
git init
git add -A
git commit -m "AI briefing viewer"
git branch -M main
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/ai-briefing.git
git push -u origin main
```
(Create the empty `ai-briefing` repo on github.com first.)

> Privacy note: GitHub Pages on a free account requires a **public** repo, so the page
> is publicly reachable by URL (not indexed, but not secret). If the briefing shouldn't
> be public, host on **Cloudflare Pages** or **Netlify** instead and enable access
> control / a password — the same files work unchanged.

### 2. Enable GitHub Pages
Repo → **Settings → Pages** → Source: **Deploy from a branch** → Branch: `main` `/ (root)`.
After ~1 minute your site is live at
`https://YOUR_GITHUB_USERNAME.github.io/ai-briefing/`.

### 3. Create a Slack Incoming Webhook
Slack → your workspace → **Apps** → add **Incoming Webhooks** → **Add to Slack** →
pick the target channel → copy the webhook URL. Then store it here (gitignored):
```bash
echo 'https://hooks.slack.com/services/XXX/YYY/ZZZ' > .slack_webhook
```

### 4. Configure and test publish.sh
Edit `PAGES_URL` at the top of `publish.sh` to your Pages URL, then:
```bash
chmod +x publish.sh
./publish.sh          # should push (if changed) and post a test message to Slack
```

### 5. Schedule it daily (launchd)
```bash
cp com.aibriefing.publish.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.aibriefing.publish.plist
launchctl start com.aibriefing.publish   # optional immediate test
```
Logs go to `publish.log`. To change the time, edit `Hour`/`Minute` in the plist,
then `launchctl unload` + `load` again.

## Alternatives

- **Slack from the cloud instead of your Mac:** use `.github/workflows/notify-slack.yml`
  (add `SLACK_WEBHOOK_URL` as a repo Actions secret, set `PAGES_URL`). It posts on every
  push, so your Mac only needs to `git push`. If you use it, delete the Slack section of
  `publish.sh` to avoid double-posting.
- **Private hosting:** Cloudflare Pages / Netlify (connect the repo or `netlify deploy
  --prod` from `publish.sh`), both with access control on the free tier.
- **Post via the Slack connector, on demand:** ask Cowork "post today's briefing to
  #channel" any morning — no webhook needed, but it's manual (the connector isn't
  reliable in unattended scheduled runs).

## Files

| File | Purpose |
|------|---------|
| `index.html` / `viewer.html` | the reader (identical; Pages serves `index.html`) |
| `briefings-data.js` | data the reader loads — rewritten daily by Cowork |
| `briefings.json` | source-of-truth JSON (last 5 briefings) |
| `publish.sh` | push to Pages + post to Slack (run on your Mac) |
| `com.aibriefing.publish.plist` | launchd job that runs `publish.sh` daily |
| `.github/workflows/notify-slack.yml` | optional cloud Slack post on push |
| `.slack_webhook` | your webhook URL (gitignored, you create it) |
