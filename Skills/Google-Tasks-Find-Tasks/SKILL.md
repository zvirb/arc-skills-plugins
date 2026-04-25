---
name: Google Tasks Find Tasks
description: Atomic node skill to find active tasks in google tasks. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Tasks Find Tasks

## Role
You are a precise tool orchestration node. Your only responsibility is to find active tasks in google tasks.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON array representing the result of the operation.
