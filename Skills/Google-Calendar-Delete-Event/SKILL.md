---
name: Google Calendar Delete Event
description: Atomic node skill to delete a calendar event. Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# Google Calendar Delete Event

## Role
You are a precise tool orchestration node. Your only responsibility is to delete a calendar event.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON object representing the result of the operation.
