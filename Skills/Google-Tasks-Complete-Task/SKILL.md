---
name: Google Tasks Complete Task
description: Atomic node skill to mark a task as complete. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Tasks Complete Task

## Role
You are a precise tool orchestration node. Your only responsibility is to mark a task as complete.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
