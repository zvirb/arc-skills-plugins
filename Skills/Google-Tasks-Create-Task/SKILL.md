---
name: google-tasks-create-task
description: "Atomic node to create a task in Google Tasks with strict validation."
allowed-tools: [exec]
---

# Google Tasks Create Task

This skill directs the agent to add a new task to a specified list using the `gog` CLI.

## Execution Directives
1. **Prepare Command:** Construct the `gog` command using the following schema:
   - `gog tasks add @default --title "<Task_Title>" [--notes "<Notes>"] [--due "<ISO_DATE>"]`
2. **Execute Script:** Wrap the command in the hardened script.
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-tasks-create-task/scripts/run.sh tasks add @default --title "..."`
3. **Verify Jidoka:** Confirm the task was created by checking for a success message or ID.
4. **Handle Failure:** If status is ERROR, report the specific reason (e.g., list not found).

## Input Schema (JSON)
```json
{
  "listId": "@default",
  "title": "Task Title",
  "notes": "Optional notes",
  "due": "2026-05-04T17:00:00Z"
}
```
