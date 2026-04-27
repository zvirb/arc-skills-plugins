---
name: Google Tasks Update Task Title
description: Atomic node skill to exclusively update the title of a task in Google Tasks.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, strictly limited to updating ONLY the title of a task, preventing schema hallucination and ensuring single-responsibility.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the update fails. You MUST evaluate the output to ensure the title was updated.

# Google Tasks Update Task Title

This skill allows the agent to update the title of an existing task in Google Tasks using the native CLI. It does NOT mark the task as complete (use Google Tasks Complete Task for that).

## Cognitive Directives
WHEN [An existing task's title needs to be modified or updated]
THEN [Invoke the `gog` tool with the argument `tasks update <tasklistId> <taskId> --title "..."`]

## Schema Example
```json
{
  "args": "tasks update @default task_id_123 --title \"Buy milk and bread\" --json"
}
```

## Jidoka Validation Loop
1. Try: Execute the command.
2. Evaluate: Check the JSON response to confirm `title` matches the requested string.
3. Correct/Fail: If it failed or hallucinated parameters, retry up to 3 times (max_retries=3) with the exact error.
4. Proceed: Return the final valid JSON.

## Expected Output
A JSON object confirming the update with the new title.
