---
name: google-tasks-find-tasks
description: "Hardened script-based execution for google-tasks-find-tasks."
allowed-tools: [exec]
---

# Google Tasks Find Tasks

This skill directs the agent to retrieve tasks from a Google Task list using the `gog` CLI directly.

## Execution Directives
1. **Execute Command**: Run the `gog` command directly.
   - Command: `gog tasks list <listId> [--status <status>] --json --results-only`
2. **Verify Output**: Ensure the response is a JSON array of tasks.
3. **Handle Failure**: If the command fails, report the error output from `gog`.

## Input Schema (JSON)
```json
{
  "listId": "@default",
  "status": "needsAction"
}
```
