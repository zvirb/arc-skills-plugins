---
name: SDLC Domain 5: Delivery
description: Workflow for deployment, plugin compilation, and agent binding.
---

# SDLC Domain 5: Delivery

This workflow guides the agent through the Delivery phase, ensuring a deterministic and traceable deployment.

# ROLE AND PHILOSOPHY
You are the **Lead System Architect**. You ensure that the production environment matches the Git source of truth. You use CLI tools for installation to prevent configuration drift.

# SOURCE OF TRUTH PROTOCOL (ALIENWARE FIRST)
> [!IMPORTANT]
> **Authority**: The OpenClaw instance on Alienware is the source of truth. It self-corrects and may have newer configurations or fixes than local files.
> **Pre-Task Check**: ALWAYS check for updates on Alienware before starting any task. Sync local files to mirror Alienware to avoid redundant work.
> **No Monolithic Overwrites**: NEVER copy a full local `openclaw.json` to Alienware. Use specific, targeted patches only.
> **State Verification**: Verify the state of files on Alienware (e.g., `cat` or `ls`) before overwriting or patching.

# EXECUTION WORKFLOW

## 1. Pre-Deployment Archive
- **Action**: Back up the current stable `openclaw.json` and `Secrets/` to `Archive/`.
- **Artifact**: Update the deployment log in `SDLC/Delivery/5.4_Version_Control.md`.

## 2. Compilation & Build
- **Action**: For plugins, execute `npm run build`.
- **Verification**: Confirm the `dist/` folder contains valid ESM code.

## 3. Standardized Installation
- **Action**: Use the OpenClaw CLI to install the component.
- **Command**: `openclaw skills install <path>` (automatically updates `openclaw.json` paths).

## 4. Agent Binding & Roster Update
- **Action**: Add the skill slug to the `agents.list[0].skills` array in `openclaw.json`.
- **Static Binding**: For workflows, bypass JIT discovery by adding skills to `tools.alsoAllow`.
- **Verification**: Restart the gateway (`openclaw restart`) and run `openclaw chat "List your tools"`.

## 5. Delivery Verification Gate (Heartbeat)
- **Action**: Execute a "Heartbeat" task using the new capability.
- **Verification**: Confirm the task completes using the **Maxwell/Pascal routing rules** defined in Design.

# MANDATORY COMPLETION
- [ ] Component installed and bound to the agent.
- [ ] Physical state of `openclaw.json` matches the Git repo.
- [ ] Heartbeat task successful.
- [ ] Git commit and sync performed.

