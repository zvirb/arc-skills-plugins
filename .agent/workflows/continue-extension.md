---
name: Continue OpenClaw Extension
description: Workflow for resuming development on an existing Skill or Plugin.
---

# Continue OpenClaw Extension

Use this workflow to resume work on an incomplete extension, ensuring no context is lost and state is properly restored.

## Steps
1. **Context Restoration:**
   - Read the relevant `SKILL.md` or Plugin source files.
   - Check `Docs/TODO.md` to understand the current progress state.
   - Read any `MEMORY.md` or `ACTIVE-TASK.md` files located in the extension's folder for durable state from previous sessions.
2. **Incremental Implementation:**
   - Proceed with modular task execution. Do not mix unrelated tasks into a single prompt.
   - Rely on "Artifacts" (e.g., code diffs, test results) to visually or programmatically verify each step before moving to the next.
3. **Validation & Testing:**
   - Write and run incremental tests in the `Tests/` directory.
   - **Critical Workflow Rule:** You MUST physically test the extension. All nodes and workflow chains must be tested end-to-end to ensure they actually work. Use native OpenClaw execution or a local `ollama` setup (like `gemma4`) to definitively prove the workflow logic.
   - Log any errors or verbose traces to the `Logs/` directory (which is safely Git-ignored).
   - If OpenClaw is running in WSL2, you MUST sync the updated skills to its workspace first (e.g., `wsl cp -r /mnt/d/openClaw/Skills/* ~/.openclaw/workspace/skills/`) before running any native `openclaw` validations.
4. **Knowledge Preservation:**
   - If a new lesson, workaround, or bug fix is discovered during the session, immediately update the extension's documentation, `Docs/context.md`, or the `SKILL.md` file (Continuous Learning directive).
5. **Next Steps:**
   - Always suggest next steps based on the user's intent in the last prompt.
6. **Git Sync:**
   - Always perform a git commit and sync (push) at the end of the workflow to persist changes.
