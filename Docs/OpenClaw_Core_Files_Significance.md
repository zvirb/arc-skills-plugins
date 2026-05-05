# OpenClaw Core Configuration Significance

This document outlines the operational significance of the core OpenClaw workspace files. These files are essential for the framework's runtime execution, identity preservation, and autonomous behavior, but they are distinct from the project's specific logic (plugins/skills).

### 🛡️ Operational Secrets (Injected Context)
These files contain PII (Personally Identifiable Information) or sensitive operational logic and are stored in the `Secrets/` directory.

| File | Significance | Role in OpenClaw |
| :--- | :--- | :--- |
| `openclaw.json` | **The Command & Control Hub** | Central configuration for AI providers, model routing, environment variables, and token limits. Required for the gateway to boot. |
| `AGENTS.md` | **The Operational Playbook** | Defines long-term rules, continuity protocols, "red lines," and how the agent handles session-to-session memory. |
| `AGENTS_ROSTER.md` | **The Workforce Ledger** | Maps agent IDs to specialized roles (Coder, Researcher, etc.) in a multi-agent environment. |
| `SOUL.md` | **The Character Constitution** | Defines the agent's personality, tone, and core values. Injected into the system prompt for behavioral consistency. |
| `IDENTITY.md` | **The Core Identity** | Contains the agent's fundamental nature, origin, and name. Works with `SOUL.md` to ground the agent's persona. |
| `HEARTBEAT.md` | **The Autonomous Pulse** | Plain-text task registry for proactive, scheduled background operations. Checked by the gateway periodically (default 30m). |
| `MEMORY.md` | **The Long-Term Retrieval Core** | Curated repository of significant insights, decisions, and lessons learned. Prevents "cognitive drift" across sessions. |
| `TOOLS.md` | **The Capability Inventory** | Local configuration for tool-specific parameters (SSH details, camera names, specific API endpoints). |
| `USER.md` | **The Human Profile** | Documents Markus's preferences, timezone, ADHD-specific needs, and bio for personalized assistance. |

### 🛠️ Runtime Assembly
At the start of every session, OpenClaw assembles the agent's "brain" by performing a **Bootstrap Injection**. The contents of these files are retrieved from `Secrets/` and injected into the LLM system prompt. This ensures that the agent:
1. **Knows Who It Is** (`SOUL`, `IDENTITY`)
2. **Knows Who It Serves** (`USER`)
3. **Remembers What Matters** (`MEMORY`)
4. **Follows the Rules** (`AGENTS`)
5. **Maintains System Health** (`HEARTBEAT`)

---
_Note: For architectural rules regarding Skill and Plugin development, see [GEMINI.md](file:///d:/openClaw/GEMINI.md)._
