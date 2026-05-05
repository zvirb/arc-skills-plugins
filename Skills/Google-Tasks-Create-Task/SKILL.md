---
name: google-tasks-create-task
description: "Atomic node to create a task in Google Tasks with strict validation."
allowed-tools: [exec]
---

# Google Tasks Create Task

This skill directs the agent to add a new task to a specified list using the `gog` CLI directly.

## Execution Directives
1. **Execute Command:** Construct and run the `gog` command directly.
   - Command: `gog tasks add @default --title "<Task_Title>" [--notes "<Notes>"] [--due "<ISO_DATE>"] --json`
2. **Verify Output:** Ensure the command returns a valid JSON response containing the new task ID.
3. **Handle Failure:** If the command fails, report the error output from `gog`.

## Input Schema (JSON)
```json
{
  "listId": "@default",
  "title": "Task Title",
  "notes": "Optional notes",
  "due": "2026-05-04T17:00:00Z"
}
```
