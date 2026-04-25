---
name: Workspace Audit Missing Meetings
description: Atomic node skill to cross-references emails for 'let's meet' with google calendar to find missing events. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Workspace Audit Missing Meetings

## Role
You are a precise tool orchestration node. Your only responsibility is to cross-references emails for 'let's meet' with google calendar to find missing events.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON string representing the result of the operation.
