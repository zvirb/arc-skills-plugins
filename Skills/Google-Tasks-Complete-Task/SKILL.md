---
name: Google Tasks Complete Task
description: Atomic node skill to complete a task in Google Tasks using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the operation fails.

# Google Tasks Complete Task

This skill allows the agent to mark a specific task as completed.

## Cognitive Directives
WHEN [A task needs to be marked as finished or completed]
THEN [Execute the `gworkspace_tasks_complete` plugin tool]

## Schema Example
```json
{
  "taskId": "task_id_123"
}
```

## Expected Output
A JSON object confirming the task completion.
