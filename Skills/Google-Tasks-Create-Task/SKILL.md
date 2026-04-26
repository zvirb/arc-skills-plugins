---
name: Google Tasks Create Task
description: Atomic node skill to create a task in Google Tasks using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if task creation fails.

# Google Tasks Create Task

This skill allows the agent to create a new task in Google Tasks.

## Cognitive Directives
WHEN [A new task needs to be added to a Google Tasks list]
THEN [Execute the `gworkspace_tasks_create` plugin tool]

## Schema Example
```json
{
  "title": "Buy milk",
  "notes": "Organic whole milk",
  "due": "2026-04-26T17:00:00Z"
}
```

## Expected Output
A JSON object confirming the task was created (including task ID).
