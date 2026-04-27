# Hybrid Skill Synchronization Workflow (Local Injection & ClawHub Re-Attachment)

## Overview
This workflow automates the deployment of OpenClaw skills across multiple machines (Laptop/Local WSL and Remote Alienware Server) bypassing ClawHub rate limits for immediate availability, while preserving the ability to update them via the official registry once published.

## Step 1: Extensive Research & Documentation Review
- **CRITICAL:** You must always research extensively online for any up-to-date information regarding how tools work and how the APIs they rely on work.
- You need to be sure that you have full understanding of schemas and all commands necessary to be passed to tools, and the full schema of any database the tool relies on to ensure full success. This requires research online for documentation to describe all these details.

## Step 2: Local Injection (Bypass Rate Limits)
Copy the latest skills from the development folder (`D:\openClaw\Skills`) directly into the OpenClaw managed workspace on all target machines. This makes them instantly available as "unmanaged" local skills.

### Action (Laptop / Local WSL)
```bash
// turbo
wsl bash -c "cp -r /mnt/d/openClaw/Skills/* ~/.openclaw/workspace/skills/"
```

### Action (Alienware Server)
```bash
// turbo
ssh alienware "mkdir -p ~/.openclaw/workspace/skills && rsync -avP marku@laptop_ip:/mnt/d/openClaw/Skills/ ~/.openclaw/workspace/skills/"
# Note: Alternatively, clone the git repo directly on Alienware to avoid SSH-from-SSH issues:
ssh alienware "git clone https://github.com/zvirb/arc-skills-plugins.git /tmp/openclaw-skills || (cd /tmp/openclaw-skills && git pull) && cp -r /tmp/openclaw-skills/Skills/* ~/.openclaw/workspace/skills/"
```

## Step 3: Check ClawHub Publication Status
Verify if the skills have been fully published to the ClawHub registry. This allows us to transition from "local unmanaged" to "ClawHub managed".

```bash
// turbo
wsl bash -c "openclaw skills search \"\""
```
*(Manually compare the returned list with the local skills to determine if they are fully published.)*

## Step 4: Re-attach to ClawHub (Regain Update Utility)
Once a skill is officially published to ClawHub, re-install it to inject the `_meta.json` tracking files. This overwrites the local copy and turns it back into a managed skill, enabling `openclaw skills update`.

### Action (Laptop / Local WSL)
```bash
// turbo
wsl bash -c "for skill in ~/.openclaw/workspace/skills/*; do openclaw skills install \$(basename \"\$skill\"); done"
```

### Action (Alienware Server)
```bash
// turbo
ssh alienware "for skill in ~/.openclaw/workspace/skills/*; do openclaw skills install \$(basename \"\$skill\"); done"
```

## Step 5: Verify Agent Binding
Installing the skills only updates the `skills.entries` registry. You MUST ensure that the `~/.openclaw/openclaw.json` file on both the Laptop and the Alienware Server has the newly injected skill slugs explicitly listed within the `agents.list[0].skills` array. Failure to do so will result in "Ghost Skills" that the gateway loads but the agent cannot see.
