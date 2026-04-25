---
name: micro-suck-generation
description: Issue minor resilience challenges to build task-initiation momentum.
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
  orchestrator: Cron
  security: None
  type: script
---

# Micro-Suck Generation

A custom skill pulls from a randomized matrix of minor, two-minute tasks (e.g., "clear the physical desktop").
When a lull in energy is detected (or triggered randomly), the system formulates the task and either presents it dynamically in the chat interface or injects it as an immediate, high-priority item at the top of today's Google Tasks list to kickstart executive function.

## Directives
- **Input:** Energy lull detection or cron trigger.
- **Process:** Select random micro-task. Inject to Google Tasks or Chat.
- **Output:** Notification of micro-task.
