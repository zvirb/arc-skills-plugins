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
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# Google Calendar Create Event

## Role
You are a precise tool orchestration node. Your only responsibility is to create a new Google Calendar event.

## Input
A JSON object with `title`, `start_time`, `end_time` (or `duration`).

## Expected Output
A JSON object confirming the creation (including the event ID).

## Loop Logic
`node.py` loops up to 3 times to create the event and validates the response object contains an ID.
