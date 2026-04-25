---
name: Gmail Delete Email
description: Atomic node skill to delete an email by id. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Gmail Delete Email

## Role
You are a precise tool orchestration node. Your only responsibility is to delete an email by id.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
