---
name: Google Drive Upload File
description: Atomic node skill to upload a file to google drive. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Drive Upload File

## Role
You are a precise tool orchestration node. Your only responsibility is to upload a file to google drive.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
