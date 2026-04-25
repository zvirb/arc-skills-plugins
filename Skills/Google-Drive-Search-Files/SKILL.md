---
name: Google Drive Search Files
description: Atomic node skill to search for files in google drive. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Drive Search Files

## Role
You are a precise tool orchestration node. Your only responsibility is to search for files in google drive.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON array representing the result of the operation.
