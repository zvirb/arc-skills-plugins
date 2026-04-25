---
name: Update OpenClaw Extension
description: Workflow for retrofitting and upgrading completed extensions to the latest best practices.
---

# Update OpenClaw Extension

Use this workflow to audit and refactor existing OpenClaw extensions to meet new architectural standards and SDK updates.

## Core Principles
All updates MUST enforce the following Lean principles:
- **Kaizen (改善):** Continuously break monolithic processes into smaller, perfectible components.
- **Standardized Work (Hyojun Sagyo):** Prerequisite to automation. Ensure the underlying manual/CLI process is the most efficient path available.
- **Jidoka (自働化):** Ensure all nodes have self-healing validation loops that halt execution if a defect (invalid output/error) is detected.

## Steps
1. **Audit Phase:**
   - Review the extension's codebase against current global directives (`GEMINI.md`, `AGENTS.md`).
   - For Skills: Check for overly complex instructions. Simplify to "one skill, one responsibility". Verify YAML frontmatter for security and environment requirements.
   - For Plugins: Verify SDK imports (`openclaw/plugin-sdk/plugin-entry`), error handling (graceful failures instead of stack traces), and `package.json` compatibility definitions.
2. **Refactoring:**
   - Apply necessary updates. Break apart monolithic skills into smaller modular skills if needed.
   - Transition any long-running, blocking plugin tasks to asynchronous operations.
   - Ensure all secrets are gated behind environment variables and are never hardcoded.
3. **Validation & Testing:**
   - Run existing tests and add new tests covering the refactored logic in `Tests/`.
   - **Critical Workflow Rule:** You MUST physically test the extension. All nodes and workflow chains must be tested end-to-end to ensure they actually work. 
   - Test LLM-driven nodes directly using native OpenClaw or by wiring in a local `ollama` model (e.g., `gemma4`) to ensure true integration resilience.
   - If OpenClaw is running in WSL2, you MUST sync the updated skills to its workspace first (e.g., `wsl cp -r /mnt/d/openClaw/Skills/* ~/.openclaw/workspace/skills/`).
   - Execute `wsl openclaw skills check` or `openclaw plugins list --verbose`.
4. **State Tracking:**
   - Document the update in the extension's `README.md` or `SKILL.md` changelog.
   - If the update resolves an outstanding issue, update `Docs/TODO.md`.
5. **Next Steps:**
   - Always suggest next steps based on the user's intent in the last prompt.
6. **Git Sync:**
   - Always perform a git commit and sync (push) at the end of the workflow to persist changes.
