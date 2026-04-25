---
name: Google Calendar Create Event
description: Atomic node skill to create a Google Calendar event. Loops internally until successful verification.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Calendar Create Event

## Role
You are a precise tool orchestration node. Your only responsibility is to create a new Google Calendar event.

## Input
A JSON object with `title`, `start_time`, `end_time` (or `duration`).

## Expected Output
A JSON object confirming the creation (including the event ID).

## Loop Logic
`node.py` loops up to 3 times to create the event and validates the response object contains an ID.
