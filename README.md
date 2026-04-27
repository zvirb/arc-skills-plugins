# Open Claw

This repository contains Skills and Plugins for Open Claw.

## Directory Structure

- `Config/`: Contains non-secret configuration files (e.g., agent settings, prompt templates).
- `Docs/`: Contains overarching project documentation, guidelines, and manuals.
- `Logs/`: Contains execution traces and agent logs. **This folder is ignored by Git.**
- `Memory/`: Persistent storage for the agent (e.g., vector databases, context logs). **Data files ignored by Git.**
- `Plugins/`: Contains native OpenClaw plugins. These are runtime extensions written in **TypeScript (ESM)** using the `@openclaw/plugin-sdk`. Each new plugin should be created in its own sub-folder with a `package.json`.
- `Scripts/`: Contains globally useful utility scripts and repository automation.
- `Secrets/`: Contains sensitive data, credentials, and API keys. **This folder is strictly ignored by Git.**
- `Skills/`: Contains OpenClaw skills. Skills are **strictly Markdown (`SKILL.md`)** cognitive modifiers teaching the agent how to use tools. NO Python `.py` orchestrators are allowed here.
- `Tests/`: Contains test suites and testing infrastructure.

## Project Tidiness & Root Folder Rules

To maintain a clean and manageable repository, please adhere to the following rules:

1. **Minimize Root Files:** Do not clutter the root folder (`/`) with scripts, temporary files, configuration snippets, or notes. The root folder should strictly contain high-level configurations (e.g., `.gitignore`, `README.md`) and the primary directories.
2. **Strict Sub-Folder Isolation:** All code, assets, and documentation for a specific skill or plugin MUST live entirely within its designated sub-folder (e.g., `Skills/MySkill/`). Do not leak skill-specific files into the root or parent directories.
3. **Use the Docs Folder:** Any overarching documentation or project-wide notes must go into the `Docs/` directory, not the root directory.
4. **Clean Up:** Regularly delete temporary files and test scripts. If a script is useful globally, consider making it a proper utility within a designated folder rather than leaving it in the root.

## Extension Installation & Deployment

When deploying an extension (Skill or Plugin) to an OpenClaw gateway, remember the following critical rule:
**Agents do NOT automatically inherit newly installed skills.** 
You must explicitly configure the `openclaw.json` manifest:
1. Install the extension via `openclaw skills install <path>` (or `plugins`).
2. Add the skill's slug into the specific agent's profile array (e.g., `agents.list[0].skills`) inside `~/.openclaw/openclaw.json`.
3. Restart the `openclaw-gateway` service.
Failure to bind the skill to the agent's profile will result in the agent being completely unaware of the capability!

## Development Standard: Research & Verification
To ensure high-fidelity automation and eliminate hallucinations:
- **Mandatory Online Research:** Always retrieve the latest API/Tool schemas from the web before implementation.
- **Independent Browser Verification:** For all Google Workspace tools, use the `browser` tool to physically confirm that actions (like task creation or email sending) were successful in the user's workspace.
