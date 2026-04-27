# Open Claw Skills Context

This folder contains Skills for Open Claw.

## Development Rules & Structure

1. **Sub-Folder Isolation:** Every new skill MUST be created in its own dedicated sub-folder within this directory.
   - Example: `Skills/MyNewSkill/`
2. **Self-Containment:** Each skill sub-folder should contain all its necessary source code, configuration files, prompts, and specific documentation.
3. **Naming Convention:** Use clear, descriptive names for your skill sub-folders.
4. **Progress Tracking:** When planning, starting, or completing a skill, you MUST update the central progress tracker located at `Docs/TODO.md`.
5. **Skill Injection & Configuration Update:** Whenever copying or injecting unmanaged local skills into the global `~/.openclaw/workspace/skills/` directory (e.g., WSL or Alienware), you MUST also update the OpenClaw configuration so the engine recognizes the newly injected skills. A simple folder copy is insufficient. **CRITICAL:** You must follow the exact installation and registration procedures defined in [`Docs/Local_Extension_Installation.md`](../Docs/Local_Extension_Installation.md).
6. **Continuous Learning:** Whenever a lesson is learned or a workaround is discovered during attempted work, you MUST immediately update this context file, the specific skill's documentation, or the relevant workflow steps to ensure the new knowledge is explicitly preserved.
7. **Mandatory Testing (The "Trust But Verify" Protocol):** You MUST physically test the extension. Test that the skill or plugin built and deployed to both alienware and local wsl open claw actually functions as it should. Reiterate until you can confirm that the tool works as expected. **CRITICAL:** You must retrieve confirmation that the tool worked. Use another tool to independently verify that the tool did what was expected. For Google Workspace tools (Gmail, Calendar, Tasks, Drive), you MUST use the `browser` tool to physically verify the state change in the user's workspace.
   - **The TUI:** Run `openclaw tui` (press `[L]` to toggle log viewer).
   - **The One-Liner:** Run `echo "Your task here" | openclaw chat`.
   - **Send and Tail Logs:** Send via `openclaw message send` and verify via `openclaw logs --follow`.
   - **Physical Verification:** Use the `browser` tool to navigate to the relevant Google Workspace URL and confirm the expected change.
8. **Extensive Research & Documentation Review:** Before implementation, you MUST research extensively online for up-to-date information regarding how tools and their underlying APIs work. You must have a full understanding of schemas, necessary commands, and database structures to ensure success.
