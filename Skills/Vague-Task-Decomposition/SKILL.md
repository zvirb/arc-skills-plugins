---
name: Vague Task Decomposition
description: Combine existing Linear skill logic with a custom prompt tailored specifically for Google Tasks API manipulation via Composio.
os: windows
requires:
  bins:
    - python
  env:
    - COMPOSIO_API_KEY
---

# Vague Task Decomposition Skill

This skill uses an LLM prompt to decompose a vague task string into actionable, distinct subtasks and then dispatches them to Google Tasks using Composio.

## Instructions
1. Accept a vague task description.
2. Formulate a prompt requesting a JSON array of actionable subtasks.
3. Call a local LLM or API to get the decomposition.
4. Iterate over the subtasks and use Composio's Google Tasks integration to create entries.
