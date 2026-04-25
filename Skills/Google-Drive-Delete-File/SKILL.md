---
name: Google Drive Delete File
description: Atomic node skill to delete a file from google drive. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Drive Delete File

## Role
You are a precise tool orchestration node. Your only responsibility is to delete a file from google drive.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
