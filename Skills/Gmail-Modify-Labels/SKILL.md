---
name: Gmail Modify Labels
description: Atomic node skill to modify labels of an email. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Gmail Modify Labels

## Role
You are a precise tool orchestration node. Your only responsibility is to modify labels of an email.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
