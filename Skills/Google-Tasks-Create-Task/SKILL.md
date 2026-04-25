---
name: Google Tasks Create Task
description: Atomic node skill to create a new task in google tasks. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Tasks Create Task

## Role
You are a precise tool orchestration node. Your only responsibility is to create a new task in google tasks.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
