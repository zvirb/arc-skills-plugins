---
name: Google Docs Read Document
description: Atomic node skill to read the contents of a google document. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Docs Read Document

## Role
You are a precise tool orchestration node. Your only responsibility is to read the contents of a google document.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
