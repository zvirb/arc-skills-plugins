---
name: Google Tasks Find Tasks
description: Atomic node skill to search for tasks in Google Tasks using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the search fails.

# Google Tasks Find Tasks

This skill allows the agent to search for active tasks in Google Tasks using the gog CLI.

## Cognitive Directives
WHEN [Requested to list tasks or find a specific task in Google Tasks]
THEN [
  Execute the following Jidoka-validated loop:
  1. **Execute Node:** Invoke the `gog` tool with the argument `tasks list <tasklistId> --json` (with optional flags like `--show-completed` or `--due-max`).
  2. **Verification Step (Jidoka):** Check if the output is a valid JSON array. IF the command fails or returns an error message, wait 3 seconds and retry (max 3 times). IF it still fails, report the error to the user and STOP.
]

## Schema Example
```json
{
  "args": "tasks list @default --json"
}
```

## Expected Output
A JSON array of task objects (id, title, notes, status).
