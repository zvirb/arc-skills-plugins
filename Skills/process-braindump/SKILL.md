---
name: kebab-case-auto-fix
description: "Triggers for processing unstructured thoughts. Prioritizes, decomposes, and routes content."
allowed-tools: [write, sessions_spawn, gog]
triggers: [process brain dump, ingest chaotic notes, unstructured thought sync]
negative-triggers: [todo list, scheduled meeting, measurement, schematic]
---

# Process Brain Dump Directive

This skill directs the agent to decompose unstructured handwritten thoughts into organized artifacts.

## Execution Directives
1. **Analyze Content:** Execute a semantic scan of the transcript to identify distinct themes (e.g., Project Ideas, Shopping Items, Philosophical Musings).
2. **Decompose & Prioritize:** Rank identified items by immediate actionability.
3. **Route Artifacts:**
   - **Actionable Tasks:** Execute `gog tasks add` for high-priority items.
   - **New Projects:** Execute `write_file` to create a new Markdown document in `workspace/explorations/` for complex ideas.
   - **General Reference:** Append to the user's `MEMORY.md` if the item is purely informational.
4. **Finalize:** Provide a map of where the various parts of the brain dump were routed.

## Expected Output
A routing report for the decomposed brain dump.
