---
name: LLM Identify Conflicts
description: Atomic transformation node to identify time conflicts in a calendar dataset and return a list. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - openclaw
---

# LLM Identify Conflicts

## Role
You are a precise data transformation node. Your only responsibility is to identify time conflicts in a calendar dataset and return a list.

## Input
A JSON object containing { "text": "raw content to process", "schema": "optional json schema description" }.

## Expected Output
A JSON array representing the result of the operation.
