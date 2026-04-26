---
name: backlog-grooming
description: Workflow-driven skill that autonomously manages stale items in Google Tasks.
os: windows
requires:
  bins:
  env:
    - COMPOSIO_API_KEY
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# Backlog Grooming

This skill orchestrates a workflow to identify and archive stale Google Tasks (items older than 30 days) to maintain a clean workspace.

## Workflow Orchestration
This skill is an autonomous workflow. You MUST chain the following atomic actions using your native tools provided by the LLMTransformations and GoogleWorkspace plugins:
1. **Google-Tasks-Find-Tasks**: Retrieves all active tasks.
2. **LLM-Summarize-Text**: Generates a concise summary of the task's intent for archiving.
3. **Google-Tasks-Update-Task**: Prepends `[STALE/ARCHIVED]` and marks the task as completed.

## Role
You are a maintenance agent. You should periodically trigger this workflow to prevent the user's task list from becoming cluttered with stale items.

## Input
None (Triggered by schedule/cron).

## Expected Output
A JSON summary of groomed tasks.
