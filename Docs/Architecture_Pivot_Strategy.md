# OpenClaw Architecture Pivot Strategy

## Overview
Historically, this project incorrectly implemented OpenClaw extensions by writing Python orchestration scripts (e.g., `node.py`, `workflow.py`) inside the `Skills/` and `Workflows/` directories. These Python scripts functioned as external orchestrators that spawned sub-shells to call `wsl openclaw infer`, effectively treating OpenClaw as a dumb LLM endpoint rather than a native agentic framework. 

This document outlines the strategy for pivoting back to true OpenClaw architecture.

## The True OpenClaw Architecture

In the native OpenClaw ecosystem, the architecture is strictly delineated into two layers:

### 1. Plugins (The Runtime Layer)
- **Role:** Add new capabilities, tools, native API endpoints, database interactions, state management, or hardware integrations.
- **Language:** Strictly TypeScript (ESM).
- **Structure:** 
  - Isolated within a subfolder in the `Plugins/` directory.
  - Requires a `package.json` with an `openclaw` object defining metadata and compatibility.
  - Must utilize the official SDK (`@openclaw/plugin-sdk`).
  - Must export a `register(api: PluginApi)` function that explicitly registers new tools (e.g., `api.registerTool({ name: 'my_tool', execute: async () => {...} })`).
- **Rule:** If it executes code, manages state, or interacts with the system, it MUST be a Plugin.

### 2. Skills (The Cognitive Layer)
- **Role:** Teach the OpenClaw agent *when* and *how* to use tools (both native and those added by Plugins), modify cognitive behavior, and define standard operating procedures (SOPs).
- **Language:** Strictly Markdown (`SKILL.md`).
- **Structure:**
  - Contains ZERO executable code (No Python, no shell scripts).
  - Isolated within a subfolder in the `Skills/` directory.
  - Must contain YAML frontmatter explicitly declaring OS requirements and required binaries (`requires: bins: []`).
- **Rule:** If it is just a set of instructions guiding the agent, it MUST be a Skill.

---

## The Pivot Plan

To correct the anti-pattern, all future development and refactoring must adhere to the following steps:

1. **Audit Existing Python "Skills":** 
   - Identify all `node.py` and Python orchestration scripts in the `Skills/` and `Workflows/` directories.
2. **Migrate Logic to TypeScript Plugins:**
   - Extract the core programmatic logic (API calls, data parsing, state management like the Tool Strategy ledger) from the Python scripts.
   - Re-implement this logic as TypeScript Plugins using the `@openclaw/plugin-sdk`.
   - Register the specific actions as discrete tools using `api.registerTool()`.
3. **Purify the Skills:**
   - Delete the legacy Python files from the `Skills/` folders.
   - Update the `SKILL.md` files to exclusively contain natural language instructions that guide the agent to use the newly registered native Plugin tools.
4. **Delete External Workflows:**
   - Remove the `Workflows/` directory full of composite Python scripts, as OpenClaw's native agentic routing should handle multi-step orchestration autonomously when given proper `SKILL.md` instructions and access to Plugin tools.

## Development Rules (Kaizen & Jidoka)
- Never create a `.py` file to orchestrate OpenClaw. 
- Build testable, atomic tools within TypeScript Plugins.
- Provide strict, schema-driven constraints in Plugin Tool definitions to prevent LLM hallucinations.

## Plugin Antipatterns & SDK Best Practices (The Native TS Pivot)
Based on OpenClaw's Lean architecture and strict isolation requirements, the following antipatterns are explicitly forbidden in all Plugins:

1. **The Sub-Shell Orchestration Anti-pattern (The Shell Escape):**
   - **Forbidden:** Using `child_process.exec` to call `wsl openclaw infer` or native bash tools (e.g., `gog`) from within a TypeScript plugin.
   - **Required:** Use native OpenClaw SDK bindings (e.g., `api.infer(prompt)`) and actual Node.js HTTP/API clients (like the native `composio-core` SDK) instead of subshelling CLI tools.
2. **Unvalidated Environment Variables (Silent Failures):**
   - **Forbidden:** Reading `process.env.API_KEY` dynamically during tool execution.
   - **Required:** Adhere to the `IPlugin` interface by exporting a `configSchema` (e.g., Zod object or JSON schema). The OpenClaw loader enforces validation at startup and passes config securely.
3. **Path Traversal & Unsafe State Persistence:**
   - **Forbidden:** Hardcoding relative escape paths (e.g., `../../../../Memory/state.json`) or creating arbitrary local files.
   - **Required:** Use the native SDK storage handlers (`api.storage.get()` / `api.storage.set()`) to manage state, allowing the host engine to route persistence securely.
4. **Monolithic Plugins & Dynamic Cross-Tooling:**
   - **Forbidden:** Blindly calling `api.executeTool('other_plugin_tool')` without type safety or manifest dependency declarations.
   - **Required:** Cross-plugin dependencies must be explicitly declared in the manifest (e.g., `dependencies: ["google-workspace-plugin"]`) so the engine resolves the DAG at boot.
