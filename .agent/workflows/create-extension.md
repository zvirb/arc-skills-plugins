---
name: Create New OpenClaw Extension
description: Best-practice workflow for scaffolding a new OpenClaw Skill or Plugin.
---

# Create New OpenClaw Extension

This workflow guides the agent through creating a new OpenClaw extension (Skill or Plugin) according to the latest architectural standards.

## Core Principles
All development MUST adhere to the following Lean principles:
- **Kaizen (改善):** Always break processes apart into their simplest, smallest components (Atomic Nodes) before building. Investigate and perfect each tiny step.
- **Standardized Work (Hyojun Sagyo):** Before automating, find the absolute most efficient, simplest way to execute the task. Optimize the node's internal logic (e.g., using `gog` before `Composio`) to eliminate waste.
- **Jidoka (自働化):** Build "autonomation" into every node. Every node must have the "intelligence" to stop immediately (via validation loops) if it detects a defect, rather than blindly continuing.

## Steps
1. **Architectural Decision (Kaizen):** 
   - Identify the user's goal and decompose it into the smallest possible atomic units.
   - If it involves orchestrating existing tools (e.g., curl, browser, Python scripts), default to a **Skill**.
   - If it requires complex application state, new API endpoints, database bridges, or native hooks, default to a **Plugin**.
2. **Scaffold Directory:**
   - Create a dedicated sub-folder in `Skills/` or `Plugins/`.
3. **Artifact Generation:**
   - **For Skills:** Generate a `SKILL.md` with concise, explicit instructions. Follow the "one skill, one responsibility" principle. Enforce security (never concatenate raw shell strings). Add `os` and `requires` (bins, env) to the YAML frontmatter.
   - **For Plugins:** Initialize `package.json` with the `openclaw` object and strict `compat` versioning. Scaffold TypeScript files using the official SDK (`openclaw/plugin-sdk/plugin-entry`) and `register(api)`. Ensure the plugin fails gracefully.
4. **Validation & Testing:**
   - Generate unit tests in the global `Tests/` directory.
   - **Critical Workflow Rule:** You MUST physically test the extension. All nodes and workflow chains must be tested end-to-end to ensure they actually work. 
   - If testing LLM inference loops, explicitly wire in `ollama` (using the local `gemma4` model) or test directly via native OpenClaw subprocesses to ensure the schema transformation works in the real world.
   - For Skills, note that `openclaw skills check` takes no arguments and runs against the configured workspace. If OpenClaw is running in WSL2, you MUST sync the new skills to its workspace first (e.g., `wsl cp -r /mnt/d/openClaw/Skills/* ~/.openclaw/workspace/skills/`) before running `wsl openclaw skills check` to verify syntax.
   - Run `openclaw plugins list --verbose` (for Plugins).
5. **State Tracking:**
   - Update `Docs/TODO.md` to list the new extension under "In Progress".
6. **Next Steps:**
   - Always suggest next steps based on the user's intent in the last prompt.
7. **Git Sync:**
   - Always perform a git commit and sync (push) at the end of the workflow to persist changes.
