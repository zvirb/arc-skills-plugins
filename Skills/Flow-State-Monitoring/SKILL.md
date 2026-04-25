---
name: flow-state-monitoring
description: Workflow-driven skill that infers deep focus and autonomously mutes interruptions.
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



# Flow State Monitoring

This skill orchestrates a workflow to analyze focus telemetry and autonomously update your status in Google Workspace to protect your flow state.

## Workflow Orchestration
This skill delegates its execution to `d:\openClaw\Workflows\flow_state_monitoring.py`, which chains the following atomic nodes:
1. **LLM-Analyze-Flow-State**: Analyzes telemetry from sensors (like `catchme`) to infer deep focus.
2. **Google-Calendar-Create-Event**: Injects a "Busy - In Flow" event to signal unavailability.

## Role
You are a focus guardian. You should monitor the user's activity and proactively trigger this workflow to prevent interruptions during deep work.

## Input
Telemetry data from local focus sensors.

## Expected Output
A confirmation of the status update.
