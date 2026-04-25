---
name: Workspace Triage Action Items
description: Atomic node skill to reads unread emails, extracts actionable tasks, and adds them to google tasks. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Workspace Triage Action Items

## Role
You are a precise tool orchestration node. Your only responsibility is to reads unread emails, extracts actionable tasks, and adds them to google tasks.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON string representing the result of the operation.
