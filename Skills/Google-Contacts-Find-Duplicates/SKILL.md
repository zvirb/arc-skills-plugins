---
name: Google Contacts Find Duplicates
description: Atomic node skill to analyze contacts to identify duplicates. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Contacts Find Duplicates

## Role
You are a precise tool orchestration node. Your only responsibility is to analyze contacts to identify duplicates.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON string representing the result of the operation.
