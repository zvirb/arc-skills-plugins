---
name: Google Tasks Find Tasks
description: Atomic node skill to search for tasks in Google Tasks using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the search fails.

# Google Tasks Find Tasks

This skill allows the agent to search for active tasks in Google Tasks.

## Cognitive Directives
WHEN [Requested to list tasks or find a specific task in Google Tasks]
THEN [Execute the `gworkspace_tasks_find` plugin tool]

## Schema Example
```json
{
  "tasklist": "@default",
  "showCompleted": false
}
```

## Expected Output
A JSON array of task objects (id, title, notes, status).
