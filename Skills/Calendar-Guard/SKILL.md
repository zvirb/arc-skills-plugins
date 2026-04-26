---
name: calendar-guard
description: Workflow-driven skill that autonomously defends your schedule to manage cognitive load and prevent burnout.
os: all
requires:
  bins: []
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.

# Calendar Guard

This skill evaluates schedule density and automatically injects recovery blocks into your Google Calendar when needed to prevent burnout.

## Cognitive Directives
WHEN [Requested to check calendar for burnout risks OR running on a daily schedule]
THEN [
  1. Execute `gworkspace_calendar_find` to retrieve events for the next 24 hours.
  2. Execute `llm_identify_conflicts` (Sub-Agent) to analyze the event list for periods of high cognitive load.
  3. IF high load is detected, Execute `gworkspace_calendar_create` to inject "Recovery Block" events to protect decompression time.
]

## Expected Output
A JSON log of any recovery blocks injected.
