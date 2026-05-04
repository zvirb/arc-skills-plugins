---
name: process-schematics
description: "Triggers for processing design changes, measurements, and diagrams. Preserves original design state."
allowed-tools: [read, write, llm-extract-json]
triggers: [process measurements, ingest schematic, design update, diagram notes]
negative-triggers: [todo list, meeting notes, journal entry, personal reflection]
---

# Process Schematics Directive

This skill directs the agent to update design documents with new measurements or design changes extracted from handwritten notes.

## Execution Directives
1. **Extract Measurements:** Execute `llm_extract_json` to isolate specific dimensions, materials, or architectural changes from the transcript.
2. **Locate Design File:** Identify the relevant `.md` or `.prose` file associated with the project (e.g., `Cooktop_Swap_Design.md`).
3. **Retrieve State:** Execute `read_file` to load the current document content.
4. **Append Change Log:** Execute `write_file` to append a "Design Revision" block at the end of the file. 
   - **Structure:** `## Revision: [Date] | [Summary of Changes]`.
   - **Constraint:** Do NOT modify any existing text above the new block.
5. **Confirm Update:** Report the specific measurements updated to the user.

## Expected Output
A confirmation of the non-destructive design update.
