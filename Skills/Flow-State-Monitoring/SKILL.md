---
name: flow-state-monitoring
description: Workflow-driven skill that infers deep focus and autonomously mutes interruptions.
os: all
requires:
  bins: []
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.

# Flow State Monitoring

This skill orchestrates a workflow to analyze focus telemetry and autonomously update your status in Google Workspace to protect your flow state.

## Cognitive Directives
WHEN [telemetry from local sensors indicates deep focus] 
THEN [Execute `llm_classify_intent` (Sub-Agent) to classify the activity. If classified as "Deep Work", Execute `gworkspace_calendar_create` with schema: { "summary": "Busy - In Flow", "status": "busy" } to block interruptions]

## Expected Output
A JSON confirmation of the calendar status update.
