---
name: Google Workspace Orchestrator
description: Manage and orchestrate Google Workspace capabilities (Gmail, Calendar, Drive, Tasks) using gog natively with a fallback to Composio for complex execution.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Workspace Orchestrator Skill

This skill provides workflow patterns and scripts to allow the agent to manage Google Workspace natively.

## Capabilities Overview
1. **Calendar & Scheduling:** Retrieve events, check conflicts, and generate new calendar blocks. Schedule a task for `X` amount of time before its due date.
2. **Gmail:** Search emails, read messages, and send outbound mail.
3. **Google Drive:** Search for documents and retrieve their contents.
4. **Google Tasks:** Retrieve active tasks or create new ones.

## Tool Chain
- **Primary Tool:** `gog` (The official Google Workspace CLI for direct integration).
- **Fallback Tool:** `composio` (Python SDK or CLI) for complex flows that `gog` might miss or if `gog` is unavailable.

## Usage
The main orchestration logic is contained in `workspace_manager.py`. It provides functions to search emails, schedule tasks dynamically by resolving calendar conflicts, and interact with Drive.
