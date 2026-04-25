---
name: Workspace Proactive Rescheduler
description: Atomic node skill to finds calendar conflicts and automatically drafts emails proposing new times. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Workspace Proactive Rescheduler

## Role
You are a precise tool orchestration node. Your only responsibility is to finds calendar conflicts and automatically drafts emails proposing new times.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON string representing the result of the operation.
