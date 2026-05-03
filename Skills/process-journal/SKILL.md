---
name: kebab-case-auto-fix
description: "Triggers for processing handwritten meeting notes or journal entries. Performs timestamped appends."
allowed-tools: [read, write]
triggers: [process handwritten journal, ingest meeting notes, append to journal]
negative-triggers: [todo list, schematic, diagram, measurement, brain dump]
---

# Process Journal Directive

This skill directs the agent to append transcribed handwritten notes to the user's persistent journal.

## Execution Directives
1. **Locate Target Document:** Determine if the notes belong to a specific meeting or the general daily journal based on content analysis.
2. **Format Entry:** Prepend a standardized Markdown header: `### Handwritten Sync - [Current Timestamp]`.
3. **Execute Append:** Execute `write_file` (append mode) to add the transcribed text to the end of the identified journal file.
4. **Verify Persistence:** Confirm the write operation was successful and report the updated file path to the user.

## Expected Output
A confirmation of the journal append operation.
