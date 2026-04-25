---
name: flow-state-monitoring
description: Infer deep focus and autonomously mute interruptions.
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

# Flow State Monitoring

The open-source `catchme` application monitors local application-switching frequencies (Alt-Tab rate).
When prolonged focus in a single application (like a terminal or CAD software) is detected, the script triggers an API call to set your OpenClaw notification threshold to "Critical Only." Additionally, it can dynamically inject a "Busy - In Flow" status into Google Chat or Google Calendar via Composio to signal unavailability to others.

## Directives
- **Input:** Telemetry from `catchme`.
- **Process:** Analyze frequency. If flow detected, set status to DND and update workspace presence.
- **Output:** Status update confirmation.
