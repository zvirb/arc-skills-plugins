---
name: calendar-guard
description: Workflow-driven skill that autonomously defends your schedule to manage cognitive load and prevent burnout.
os: windows
requires:
  bins:
    - python
  env:
    - COMPOSIO_API_KEY
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# Calendar Guard

This skill orchestrates a workflow to evaluate schedule density and automatically inject recovery blocks into your Google Calendar when needed.

## Workflow Orchestration
This skill delegates its execution to `d:\openClaw\Workflows\calendar_guard.py`, which chains the following atomic nodes:
1. **Google-Calendar-Find-Event**: Retrieves events for the next 24 hours.
2. **LLM-Identify-Conflicts**: Analyzes the event list to identify periods of high cognitive load.
3. **Google-Calendar-Create-Event**: Injects "Recovery Block" events to protect decompression time.

## Role
You are a protective agent. You should monitor the user's calendar and proactively trigger this workflow to prevent burnout.

## Input
None (Evaluates current calendar state).

## Expected Output
A JSON log of any recovery blocks injected.
