---
name: Google Tasks Create Subtask
description: Atomic node skill to create a subtask under a specific parent task in Google Tasks using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if task creation fails.

# Google Tasks Create Subtask

This skill allows the agent to create a new subtask under an existing parent task in Google Tasks using the native CLI.

## Cognitive Directives
WHEN [A task needs to be added as a subtask under another parent task in Google Tasks]
THEN [Invoke the `gog` tool with the argument `tasks add <tasklistId> --title "Subtask Title" --parent "<parentTaskId>" --notes "Optional Notes" --due "ISO-Date"`]

**CRITICAL ANTI-HALLUCINATION WARNING:** 
The `gogcli` tool does NOT support batch creation or the `--add` flag. You MUST create subtasks ONE AT A TIME. If you need to create multiple subtasks, you must make multiple separate tool calls in sequence. Never use `--add`.

## Schema Example
```json
{
  "args": "tasks add @default --title \"Buy milk\" --parent \"T25hX2s4N19BbzBpejJz\" --notes \"Organic whole milk\" --json"
}
```

## Jidoka Validation Loop
1. Try: Execute the command.
2. Evaluate: Check the JSON response to confirm the task was created and has the correct `parent` ID.
3. Correct/Fail: If it failed or hallucinated parameters, retry up to 3 times (max_retries=3) with the exact error.
4. Proceed: Return the final valid JSON.

## Expected Output
A JSON object confirming the subtask was created (including the new task ID and parent ID).
