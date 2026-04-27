# Publish and Install OpenClaw Extensions (Skills & Plugins)

## Overview
This workflow governs the process of publishing OpenClaw skills and plugins to ClawHub, the official registry, and installing/updating them within the local OpenClaw runtime (running in WSL).

### Batch vs Individual Publishing
*   **Skills:** Can be published in batch (as a "bundle") using the `clawhub sync` command, which scans local directories and publishes new/updated skills. They can also be published individually.
*   **Plugins:** Must be published individually using `clawhub package publish`. There is currently no official "sync" command for multiple plugin packages at once.

---

## Step 1: Extensive Research & Documentation Review
- **CRITICAL:** You must always research extensively online for any up-to-date information regarding how tools work and how the APIs they rely on work.
- You need to be sure that you have full understanding of schemas and all commands necessary to be passed to tools, and the full schema of any database the tool relies on to ensure full success. This requires research online for documentation to describe all these details.

## Step 2: Authentication & User Setup
ClawHub requires an authenticated session to publish packages.

1.  **Verify Authentication Status:**
    The CLI will automatically use your stored token. You can verify this by running:
    ```bash
    wsl npx -y clawhub whoami
    ```

---

## Step 3: Publishing Skills to ClawHub
OpenClaw skills (directories containing `SKILL.md`) can be published to the registry.

**Option A: Automated Batch Publishing (Recommended)**
Use the `sync` command with explicit directory flags to automatically scan, auto-bump versions, and publish only the skills in this repository.

Copy and run this in your WSL terminal (from the project root):
```bash
wsl npx -y clawhub sync --workdir . --dir Skills
```

> [!WARNING]
> **ClawHub Rate Limits:**
> ClawHub's backend servers strictly enforce a rate limit of **max 5 NEW skills per hour** for standard accounts to prevent spam.
> If you have a large batch of new skills, the command will fail with `Uncaught ConvexError: Rate limit: max 5 new skills per hour`. You will need to run this `sync` command periodically (e.g., once an hour) until all new skills are uploaded. Updates to *existing* skills do not count towards this limit.

**Option B: Individual Publishing**
Publish a specific skill folder manually.
```bash
wsl npx -y clawhub publish <path_to_skill_folder>
```
*Example: `wsl npx -y clawhub publish Skills/MyCustomSkill`*

---

## Step 4: Publishing Plugins to ClawHub
Plugins add new code capabilities and must be published individually.

1.  Navigate to the specific plugin directory or point to it directly.
2.  Publish the package:
    ```bash
    wsl npx -y clawhub package publish <path_to_plugin_folder>
    ```
3.  Repeat for all customized plugins in the `Plugins/` directory.

---

## Step 5: Installing & Updating Locally (WSL)
Once published, or to synchronize your local OpenClaw daemon with the latest registry updates, you must install or update them via the native `openclaw` CLI.

**Updating Installed Skills:**
Update all currently installed skills from ClawHub:
```bash
wsl bash -c "openclaw skills update --all"
```

**Installing New Skills:**
```bash
wsl openclaw skills install <skill-slug>
```

**Installing/Updating Plugins:**
Install a plugin from the registry:
```bash
wsl bash -c "openclaw plugins install <plugin-name>"
```
*(Note: If testing locally developed plugins without publishing, you can use the link flag: `openclaw plugins install --link /path/to/plugin`)*

> [!WARNING]
> **CRITICAL DEPLOYMENT STEP:** Running the install command registers the capability, but agents do not inherit it automatically. You MUST manually open `~/.openclaw/openclaw.json` and append the new `<skill-slug>` to your target agent's profile (e.g., `agents.list[0].skills`) before the agent can utilize it.

---

## Step 6: Post-Installation Validation & Repair
After updating plugins or skills, ensure the daemon is healthy.

1.  **Restart Gateway (if plugins changed):**
    ```bash
    wsl openclaw gateway restart
    ```
2.  **Verify Installations:**
    ```bash
    wsl openclaw skills list
    ```
    ```bash
    wsl bash -c "openclaw plugins list"
    ```
3.  **Run Diagnostics (Jidoka principle):**
    Run the doctor tool to ensure no dependencies were broken during the update.
    ```bash
    wsl openclaw doctor
    ```
    If issues are found, the agent can attempt `wsl openclaw doctor --fix`.
