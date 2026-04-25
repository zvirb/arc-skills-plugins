---
name: Google Sheets Read Range
description: Atomic node skill to read a range of values from a spreadsheet. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Sheets Read Range

## Role
You are a precise tool orchestration node. Your only responsibility is to read a range of values from a spreadsheet.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
