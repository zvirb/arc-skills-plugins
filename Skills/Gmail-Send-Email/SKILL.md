---
name: Gmail Send Email
description: Atomic node skill to send a new email. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Gmail Send Email

## Role
You are a precise tool orchestration node. Your only responsibility is to send a new email.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
