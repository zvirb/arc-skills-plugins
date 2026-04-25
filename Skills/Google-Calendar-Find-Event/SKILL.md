---
name: Google Calendar Find Event
description: Atomic node skill to find a specific Google Calendar event. It loops internally until a valid event payload is returned via gog or Composio.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Calendar Find Event

## Role
You are a precise tool orchestration node. Your only responsibility is to find a Google Calendar event.

## Input
A JSON object with search criteria (e.g., date range, keywords).

## Expected Output
A JSON array of valid events.

## Loop Logic
The included `node.py` script automatically retries the search operation using `gog` (fallback: `composio`) up to 3 times, validating that the output matches the expected JSON structure before succeeding.
