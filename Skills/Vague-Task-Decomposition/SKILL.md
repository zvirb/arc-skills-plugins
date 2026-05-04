---
name: vague-task-decomposition
description: Atomic node to break complex tasks into actionable subtasks.
os: all
requires:
  bins: [gog]
---

# Vague Task Decomposition

This skill directs the agent to transform a broad task into a sequence of actionable items.

## Execution Directives
1. **Decompose Task:** Execute `llm_extract_action_items` on the vague task description.
2. **Verify Subtasks:** Ensure the output contains a list of distinct, actionable steps.
3. **Request Approval:** Present the list of subtasks to the user. Wait for explicit "Approved" feedback.
4. **Commit to Tasks:** After approval, execute `gog tasks add @default --title "<Subtask>"` for each item.
5. **Finalize:** Report a confirmation of the newly created subtasks.

## Expected Output
A JSON summary of the subtasks successfully added to Google Tasks.
