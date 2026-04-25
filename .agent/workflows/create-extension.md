---
name: Create New OpenClaw Extension
description: Best-practice workflow for scaffolding a new OpenClaw Skill or Plugin.
---

# Create New OpenClaw Extension

This workflow guides the agent through creating a new OpenClaw extension (Skill or Plugin) according to the latest architectural standards.

## Steps
1. **Architectural Decision:** 
   - Identify the user's goal.
   - If it involves orchestrating existing tools (e.g., curl, browser, Python scripts), default to a **Skill**.
   - If it requires complex application state, new API endpoints, database bridges, or native hooks, default to a **Plugin**.
2. **Scaffold Directory:**
   - Create a dedicated sub-folder in `Skills/` or `Plugins/`.
3. **Artifact Generation:**
   - **For Skills:** Generate a `SKILL.md` with concise, explicit instructions. Follow the "one skill, one responsibility" principle. Enforce security (never concatenate raw shell strings). Add `os` and `requires` (bins, env) to the YAML frontmatter.
   - **For Plugins:** Initialize `package.json` with the `openclaw` object and strict `compat` versioning. Scaffold TypeScript files using the official SDK (`openclaw/plugin-sdk/plugin-entry`) and `register(api)`. Ensure the plugin fails gracefully.
4. **Validation:**
   - Generate unit tests in the global `Tests/` directory.
   - For Skills, note that `openclaw skills check` (run via WSL if openclaw is only in WSL) takes no arguments. You may run it globally, but rely primarily on your Python unit tests to verify logic.
   - Run `openclaw plugins list --verbose` (for Plugins).
5. **State Tracking:**
   - Update `Docs/TODO.md` to list the new extension under "In Progress".
6. **Next Steps:**
   - Always suggest next steps based on the user's intent in the last prompt.
7. **Git Sync:**
   - Always perform a git commit and sync (push) at the end of the workflow to persist changes.
