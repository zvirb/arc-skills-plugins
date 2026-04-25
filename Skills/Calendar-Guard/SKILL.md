---
name: calendar-guard
description: Autonomously defend your schedule to manage cognitive load and prevent burnout.
version: 1.0.0
os:
  - windows
  - linux
  - darwin
requires:
  bins:
    - python
  env:
    - COMPOSIO_API_KEY
metadata:
  orchestrator: OpenProse
  security: None
  type: daemon
---

# Calendar Guard

The script evaluates the density of the schedule via the GOG skill's read-access to Google Calendar.
If it detects continuous meeting blocks exceeding a physiological threshold, the script injects a hardcoded "Recovery Block" event directly into Google Calendar via Composio. This blocks the time slot system-wide, preventing external booking links or colleagues from scheduling over required decompression time.

## Directives
- **Input:** Calendar events data.
- **Process:** Calculate continuous busy time. If > threshold (e.g., 3 hours), inject "Recovery Block".
- **Output:** JSON logs of injected blocks.
