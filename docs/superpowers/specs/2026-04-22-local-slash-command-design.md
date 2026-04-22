# Design: Local Slash Command + Telegram Channel Approval

**Date:** 2026-04-22  
**Status:** Approved

## Problem

Claude Code Routines (CCR) block outbound connections to `api.telegram.org`, making the existing cloud-based hunt and approve agents unable to send or receive Telegram messages. The machine running this project is not always on, ruling out always-on alternatives like a VPS or GitHub Actions as the primary workflow.

## Solution

Replace the two CCR routines with:
- A single `/hunt-events` slash command triggered manually from within Claude Code
- Automatic Telegram-based approval handled via Claude Code Channels (the official Telegram plugin)

When Claude Code is running with the Telegram channel active, Oliver's "add 1 3" reply in Telegram is delivered directly into the Claude session. Claude processes it and adds the approved events to Google Calendar via the existing MCP connector. No second slash command needed.

When the machine is off, nothing runs — accepted limitation.

## Components

### 1. `.claude/commands/hunt-events.md`

Slash command file. Adapted from `HUNT_AGENT.md` for local execution:
- Uses absolute path `~/source/ai_event_hunter/`
- Sources `.env` for Telegram credentials
- Activates `venv/bin/python` for script calls
- Follows the same 6-step flow: read state → search → filter → build JSON → post digest → commit state

### 2. `.claude/CLAUDE.md`

Project-level Claude instructions. Tells Claude how to handle incoming Telegram messages via the Channel:
- Recognise "add X Y" or "add all" as an approval command
- Read `state.json` to resolve pending events by number
- Add each approved event to the "AI Events" Google Calendar via the MCP connector
- Commit updated `state.json` with message `state: approve YYYY-MM-DD`
- Ignore any Telegram message that is not an add command

### 3. `AGENTS.md` update

Replace CCR routine links with local setup instructions:
- How to start Claude with the Telegram channel enabled
- How to run `/hunt-events`
- What to reply in Telegram to approve events

## Data Flow

```
Oliver runs /hunt-events
  → Claude searches web (8 queries from config.py)
  → Claude filters results per FILTER_INSTRUCTIONS
  → Claude calls: venv/bin/python post_digest.py --events '<json>'
      → Telegram digest posted
      → state.json updated (pending_events, seen_event_ids)
  → Claude commits state.json

Oliver replies "add 1 3" in Telegram
  → Telegram Channel delivers message to Claude session
  → Claude reads state.json pending_events
  → Claude adds event 1 and 3 to Google Calendar (AI Events calendar)
  → Claude removes approved events from pending_events
  → Claude commits state.json
```

## What Does Not Change

- `post_digest.py` — called as-is
- `check_replies.py` — no longer used (Channel replaces polling)
- `telegram_api.py` — used by post_digest.py, unchanged
- `state_manager.py` — unchanged
- `config.py` — unchanged
- `state.json` schema — unchanged

## Google Calendar Access

The Google Calendar MCP connector (`https://calendarmcp.googleapis.com/mcp/v1`) is already configured on the user's claude.ai account and is available in local Claude Code sessions. No additional setup required.

## Telegram Channel Setup (one-time)

1. Install plugin: `/plugin install telegram@claude-plugins-official`
2. Configure token: `/telegram:configure <bot_token>`
3. Start with channel: `claude --channels plugin:telegram@claude-plugins-official`
4. Pair account: message the bot → get code → `/telegram:access pair <code>` → `/telegram:access policy allowlist`
