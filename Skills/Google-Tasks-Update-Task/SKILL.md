---
name: Google Tasks Update Task
description: Atomic node skill to update a task in Google Tasks using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the update fails.

# Google Tasks Update Task

This skill allows the agent to update an existing task in Google Tasks using the native CLI.

## Cognitive Directives
WHEN [An existing task needs to be modified or updated]
THEN [Execute the native terminal command `gog tasks update <tasklistId> <taskId> --title "..." --status "..."`]

## Schema Example
```json
{
  "command": "gog tasks update @default task_id_123 --title \"Buy milk and bread\" --status \"needsAction\" --json"
}
```

## Expected Output
A JSON object confirming the update.
