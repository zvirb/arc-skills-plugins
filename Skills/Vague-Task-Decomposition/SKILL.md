---
name: Vague Task Decomposition
description: Standard Operating Procedure (SOP) to decompose vague tasks into actionable subtasks via atomic nodes.
os: all
requires:
  bins:
    - gog
  plugins:
    - llm-transformations-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This workflow relies entirely on discrete, single-responsibility atomic nodes rather than a monolithic loop.
- **Standardized Work (Hyojun Sagyo):** This node represents a strict, step-by-step Standard Operating Procedure (SOP) for task decomposition.
- **Jidoka (自働化):** Includes autonomous self-healing loops with hard verification stops between every step.

# Vague Task Decomposition SOP

This procedure guides the agent to decompose vague tasks and dispatch them to Google Tasks using explicitly defined atomic nodes.

## Cognitive Directives
WHEN [A task is too vague or complex to be executed directly]
THEN [
  Follow this strict Standard Operating Procedure:

  **Step 1: Task Decomposition**
  - Execute the `LLM-Extract-Action-Items` atomic skill to generate a list of discrete subtasks.
  - **Jidoka Stop:** Verify the skill returns a properly formatted list of actionable items. IF the output is invalid, retry the extraction. Do NOT proceed without a valid list.

  **Step 2: Task Dispatch**
  - Create the parent vague task using `Google Tasks Create Task` if it doesn't already exist.
  - **Jidoka Stop:** Verify the parent task was created and you have its `id`.
  - For each subtask identified in Step 1:
    - Execute the `Google Tasks Create Subtask` atomic node to log the item in Google Tasks, providing the parent task's `id` as `--parent`.
    - **Jidoka Stop:** Verify the atomic node returns a successful JSON response. IF it fails for any item, retry the creation for that specific item up to 3 times before moving to the next.
]

## Expected Output
A JSON summary of the subtasks successfully created in Google Tasks.
