---
name: kebab-case-auto-fix
description: "Triggers for processing handwritten todo lists. Performs delta-check and non-destructive appends."
allowed-tools: [read, write, llm-extract-json]
triggers: [process handwritten tasks, ingest todo list, sync handwritten notes]
negative-triggers: [meeting notes, journal entry, measurement, schematic, drawing]
---

# Process Tasks Directive

This skill directs the agent to synchronize transcribed handwritten tasks with the master todo list.

## Execution Directives
1. **Identify New Tasks:** Execute `llm_extract_json` on the input payload to extract a list of task objects (title, priority).
2. **Retrieve Master List:** Execute `read_file` on `~/Documents/MASTER_TASKS.md`.
3. **Compare & De-duplicate:** Identify tasks from the handwritten list that do not already exist in the master list using semantic comparison.
4. **Append New Items:** For each unique new task, execute `write_file` (append mode) to add the item to the bottom of the master list.
5. **Report Result:** Notify the caller of the number of new tasks synchronized and any duplicates ignored.

## Expected Output
A summary of the task synchronization result.
