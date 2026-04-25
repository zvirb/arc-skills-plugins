---
name: backlog-grooming
description: Autonomously manage stale items in Google Tasks.
version: 1.0.0
os:
  - windows
  - linux
  - darwin
requires:
  bins:
    - python
  env:
    - COMPOSIO_API_KEY
metadata:
  orchestrator: Cron
  security: None
  type: script
---

# Backlog Grooming

A chron-triggered skill that wakes up on a defined schedule and queries the Google Tasks API for incomplete items older than 30 days via Composio.
The LLM reads the stale tasks, generates a one-sentence summary of the blocked intent, prepends [STALE/ARCHIVED] to the title, and either moves it to a designated "Archive" task list or marks it as completed to keep the active workspace clean.

## Directives
- **Input:** None (Triggered by Cron).
- **Process:** Query Google Tasks. Identify tasks older than 30 days. Re-summarize and prefix with [STALE/ARCHIVED]. Move or complete.
- **Output:** JSON summary of groomed tasks.
