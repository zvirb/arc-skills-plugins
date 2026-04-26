---
name: Google Calendar Find Event
description: Atomic node skill to find a specific Google Calendar event. It loops internally until a valid event payload is returned via gog or Composio.
os: windows
requires:
  bins:
    - gog
  env:
    - COMPOSIO_API_KEY
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# Google Calendar Find Event

## Role
You are a precise tool orchestration node. Your only responsibility is to find a Google Calendar event.

## Input
A JSON object with search criteria (e.g., date range, keywords).

## Expected Output
A JSON array of valid events.

## Loop Logic
The included `node.py` script automatically retries the search operation using `gog` (fallback: `composio`) up to 3 times, validating that the output matches the expected JSON structure before succeeding.
