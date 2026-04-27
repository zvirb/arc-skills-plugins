# Open Claw Plugins Context

This folder contains Plugins for Open Claw.

## Development Rules & Structure

1. **Sub-Folder Isolation:** Every new plugin MUST be created in its own dedicated sub-folder within this directory.
   - Example: `Plugins/MyNewPlugin/`
2. **Self-Containment:** Each plugin sub-folder should contain all its necessary source code, configuration files, manifests, and specific documentation.
3. **Naming Convention:** Use clear, descriptive names for your plugin sub-folders.
4. **Progress Tracking:** When planning, starting, or completing a plugin, you MUST update the central progress tracker located at `Docs/TODO.md`.
5. **Compilation Requirement:** Since plugins are written in TypeScript, you MUST compile them (`npm run build`) before attempting to install or load them. Ensure the entry point in `package.json` points to the compiled JavaScript (`dist/`), not the raw TypeScript.
6. **Extension Injection & Configuration Update:** Whenever copying or injecting unmanaged local skills or plugins into the global OpenClaw runtime environments (e.g., WSL or Alienware), you MUST also update the OpenClaw configuration so the engine recognizes them. A simple folder copy is insufficient. **CRITICAL:** You must follow the exact installation and registration procedures defined in [`Docs/Local_Extension_Installation.md`](../Docs/Local_Extension_Installation.md).
7. **Continuous Learning:** Whenever a lesson is learned or a workaround is discovered during attempted work, you MUST immediately update this context file, the specific plugin's documentation, or the relevant workflow steps to ensure the new knowledge is explicitly preserved.
8. **Mandatory Testing (The "Trust But Verify" Protocol):** You MUST physically test the extension. Test that the skill or plugin built and deployed to both alienware and local wsl open claw actually functions as it should. Reiterate until you can confirm that the tool works as expected. **CRITICAL:** You must retrieve confirmation that the tool worked. Use another tool to independently verify that the tool did what was expected. For Google Workspace tools (Gmail, Calendar, Tasks, Drive), you MUST use the `browser` tool to physically verify the state change in the user's workspace.
   - **The TUI:** Run `openclaw tui` (press `[L]` to toggle log viewer).
   - **The One-Liner:** Run `echo "Your task here" | openclaw chat`.
   - **Send and Tail Logs:** Send via `openclaw message send` and verify via `openclaw logs --follow`.
   - **Physical Verification:** Use the `browser` tool to navigate to the relevant Google Workspace URL and confirm the expected change.
9. **Extensive Research & Documentation Review:** Before implementation, you MUST research extensively online for up-to-date information regarding how tools and their underlying APIs work. You must have a full understanding of schemas, necessary commands, and database structures to ensure success.
## Plugin Antipatterns & SDK Best Practices (The Native TS Pivot)
Based on OpenClaw's Lean architecture and strict isolation requirements, the following antipatterns are explicitly forbidden in all Plugins:

1. **The Sub-Shell Orchestration Anti-pattern (The Shell Escape):**
   - **Forbidden:** Using `child_process.exec` to call `wsl openclaw infer` or native bash tools (e.g., `gog`).
   - **Required:** Use native OpenClaw SDK bindings (e.g., `api.infer(prompt)`) and actual Node.js HTTP/API clients (like the native `composio-core` SDK) instead of subshelling CLI tools.
2. **Unvalidated Environment Variables (Silent Failures):**
   - **Forbidden:** Reading `process.env.API_KEY` dynamically during tool execution.
   - **Required:** Adhere to the `IPlugin` interface by exporting a `configSchema` (e.g., Zod object). The OpenClaw loader will enforce validation at startup and pass config securely.
3. **Path Traversal & Unsafe State Persistence:**
   - **Forbidden:** Hardcoding relative escape paths (e.g., `../../../../Memory/state.json`) or creating arbitrary local files.
   - **Required:** Use the native SDK storage handlers (`api.storage.get()` / `api.storage.set()`) to manage state, allowing the host engine to route persistence securely.
4. **Monolithic Plugins & Dynamic Cross-Tooling:**
   - **Forbidden:** Blindly calling `api.executeTool('other_plugin_tool')` without type safety or manifest dependency declarations.
   - **Required:** Cross-plugin dependencies must be declared in the manifest so the engine resolves the DAG at boot.
