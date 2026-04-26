---
name: backlog-grooming
description: Workflow-driven skill that autonomously manages stale items in Google Tasks.
os: windows
requires:
  bins: []
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.

# Backlog Grooming

This skill directs the agent to trigger the native programmatic backlog grooming plugin to maintain a clean workspace.

## Cognitive Directives
WHEN [Triggered by schedule or user request to groom backlog] 
THEN [Execute the `workflow_backlog_grooming` plugin tool, which autonomously finds, summarizes via sub-agent, and archives tasks older than 30 days]

## Expected Output
A JSON summary of the groomed tasks returned by the plugin.
