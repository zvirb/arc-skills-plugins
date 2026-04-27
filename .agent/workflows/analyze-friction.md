# Analyze Friction and Generate Skills

This workflow guides the agent through analyzing provided text (such as conversation logs, user feedback, or error traces) to identify friction points, and proposing/scaffolding OpenClaw skills or plugins to eliminate that friction.

## Goal
To continuously improve the OpenClaw ecosystem by identifying areas where agents fail, get stuck, hallucinate, or cause user frustration (friction), and mapping those to new Standardized Work and Jidoka loops.

## Steps

### Step 1: Friction Identification
- Read the provided text or logs.
- Identify specific moments where:
  - The agent hallucinated commands or parameters.
  - The agent stopped autonomously and required human intervention unnecessarily.
  - The agent lacked context across different domains (e.g., cross-referencing email and calendar).
  - The user had to perform manual steps that could have been automated.

### Step 2: Gap Analysis (Check Existing Skills)
- Check the `Skills/` and `Plugins/` directories to determine if a skill already exists for this task but failed due to cognitive drift, or if a completely new skill is required.
- **Rule:** If a skill exists, propose updating it. If it doesn't, propose a new one.

### Step 3: Extensive Research & Documentation Review
- **CRITICAL:** You must always research extensively online for any up-to-date information regarding how tools work and how the APIs they rely on work.
- You need to be sure that you have full understanding of schemas and all commands necessary to be passed to tools, and the full schema of any database the tool relies on to ensure full success. This requires research online for documentation to describe all these details.

### Step 4: Propose Solutions (Lean Principles)
- Present the user with a structured analysis mapping the friction to Lean principles:
  - **The Friction:** What went wrong.
  - **The Standardized Work (Hyojun Sagyo):** The atomic node sequence needed to fix it.
  - **The Jidoka (Autonomation):** The self-healing loop required to prevent it from happening again.
- Suggest 1-3 specific Skills or Plugins to build/update.

### Step 5: Propose Automation Options
- Analyze whether the proposed skills should be triggered manually by the user, or if they should operate **automatically** (e.g., triggered by chron jobs, email webhooks, or background monitors).
- Provide the user with explicit options for automation. Example: 
  - *Option A: On-Demand Skill (Triggered explicitly in chat).*
  - *Option B: Background Automation (Triggered by a chron schedule, webhook, or background polling).*

### Step 6: Scaffold upon Approval
- Wait for the user to approve a specific skill/update and the desired automation level.
- Upon approval, immediately execute the `/Create New OpenClaw Extension` or `/Update OpenClaw Extension` workflow to scaffold the chosen solution.
- Ensure any automation requirements (like chron schedules or background triggers) are explicitly documented in the resulting `SKILL.md` or `package.json`.
