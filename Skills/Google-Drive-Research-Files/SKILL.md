---
name: Google Drive Research Files
description: Atomic node skill to search drive and extract deep research insights. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Drive Research Files

## Role
You are a precise tool orchestration node. Your only responsibility is to search drive and extract deep research insights.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON string representing the result of the operation.
