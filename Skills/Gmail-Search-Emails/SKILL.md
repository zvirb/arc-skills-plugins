---
name: Gmail Search Emails
description: Atomic node skill to search for emails. Loops internally until a valid array of email headers is retrieved.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Gmail Search Emails

## Role
You are a precise tool orchestration node. Your only responsibility is to search Gmail for matching emails.

## Input
A search query string.

## Expected Output
A JSON array of email IDs/snippets matching the query.
