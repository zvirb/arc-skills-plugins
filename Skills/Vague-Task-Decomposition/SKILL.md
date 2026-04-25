---
name: Vague Task Decomposition
description: Workflow-driven skill that decomposes vague task strings into actionable subtasks and dispatches them to Google Tasks.
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



# Vague Task Decomposition

This skill orchestrates a workflow to decompose vague task descriptions into actionable items using an LLM and then creates those items as tasks in Google Tasks.

## Workflow Orchestration
This skill delegates its execution to `d:\openClaw\Workflows\vague_task_decomposition.py`, which chains the following atomic nodes:
1. **LLM-Extract-Action-Items**: Transforms the vague string into a JSON array of subtasks.
2. **Google-Tasks-Create-Task**: Iterates through the array and creates each task via `gog` or `composio`.

## Role
You are an orchestrator. When a user provides a vague task, you should trigger the decomposition workflow to ensure the resulting tasks are granular and actionable.

## Input
A string representing a vague or complex task.

## Expected Output
A summary of the created Google Tasks.
