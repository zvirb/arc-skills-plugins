---
name: Google Contacts Create
description: Atomic node skill to create a new google contact. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Contacts Create

## Role
You are a precise tool orchestration node. Your only responsibility is to create a new google contact.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
