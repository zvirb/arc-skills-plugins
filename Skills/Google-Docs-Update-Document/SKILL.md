---
name: Google Docs Update Document
description: Atomic node skill to update the contents of a google document. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Docs Update Document

## Role
You are a precise tool orchestration node. Your only responsibility is to update the contents of a google document.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
