---
name: Vague Task Decomposition
description: Workflow-driven skill that decomposes vague task strings into actionable subtasks and dispatches them to Google Tasks.
os: all
requires:
  plugins:
    - google-workspace-plugin
    - llm-transformations-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugins' self-healing loops and will report errors if decomposition or task creation fails.

# Vague Task Decomposition

This skill orchestrates a workflow to decompose vague task descriptions into actionable items using an LLM and then creates those items as tasks in Google Tasks.

## Cognitive Directives
WHEN [A task is too vague or complex to be executed directly]
THEN [Execute the decomposition workflow:
  1. Call `llm_extract_action_items` to generate a list of subtasks.
  2. For each subtask, call `gworkspace_tasks_create` to log it in Google Tasks.]

## Schema Example
```json
{
  "task": "Plan the annual company retreat"
}
```

## Expected Output
A JSON summary of the subtasks created in Google Tasks.
