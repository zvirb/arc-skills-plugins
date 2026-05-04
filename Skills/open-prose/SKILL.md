---
name: open-prose
description: OpenProse VM orchestrator for multi-agent workflows.
metadata:
  openclaw:
    ingestion_mode: "map-reduce"
    load_on_demand: ["compiler.md", "prose.md", "help.md"]
---

# OpenProse Execution Directive

This skill directs the agent to function as the OpenProse Virtual Machine (VM) for AI sessions.

## Execution Directives

1. **Initialize VM Environment:**
   - On activation, execute `read_file` on `prose.md` and `state/filesystem.md` to load the VM core logic.
   - Do NOT load `compiler.md` or `help.md` unless explicitly requested by a `prose compile` or `prose help` command.

2. **Route Command Intent:**
   - **`prose run <file>`**: 
     - 1. Execute `read_file` on the target `.prose` file in 2,048 token chunks.
     - 2. Map `session` statements to `sessions_spawn` tool calls.
     - 3. Execute sequential statements, narrating state using the [Position] protocol.
   - **`prose compile <file>`**: 
     - 1. Execute `read_file` on `compiler.md`.
     - 2. Perform validation and report errors. 
     - 3. IMMEDIATELY clear the compiler context after execution to preserve PLE bandwidth.
   - **`prose help`**: Execute `read_file` on `help.md` and present relevant sections.

3. **Manage Program State:**
   - Execute `read` and `write` for `.prose/runs/` state persistence.
   - For PostgreSQL or SQLite modes, verify CLI availability (`psql` or `sqlite3`) before attempting connection.

4. **Handle Remote Programs:**
   - For `http://` or `https://` URLs, execute `web_fetch` to retrieve the program content.
   - Process remote files using the same map-reduce chunking strategy as local files.

## Governance Rules
- **Chunked Ingestion:** Never read more than 2,000 lines of a `.prose` file into a single prompt.
- **Strict Narration:** Use only third-person imperative logs for execution steps.
- **Memory Protection:** Clear intermediate simulation states every 5 program cycles.

## Expected Output
A structured narration of the Prose program execution and a final success/failure report.
