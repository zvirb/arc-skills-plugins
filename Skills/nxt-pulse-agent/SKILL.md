---
name: kebab-case-auto-fix
description: Proactive productivity skill with ADHD micro-stepping support.
---

# Next Pulse Agent (NXT)

This skill directs the agent to proactively manage user energy and task momentum.

## Execution Directives
1. **Analyze Session Context:** 
   - Execute a semantic scan of recent logs and `MEMORY.md`.
   - Identify active energy level: 🟢 (High), 🟡 (Moderate), or 🔴 (Low/Drained).
2. **Perform Pulse Check:** 
   - If a pulse has not occurred in the last 4 hours (check `memory/pulse-state.json`), initiate a proactive check-in.
   - **Critical Override:** If a deadline is detected within `< 6 hours`, bypass energy checks and alert the user immediately.
3. **Execute Energy-Appropriate Nudge:**
   - 🟢/🟡 Energy: Propose a high-impact task from the backlog.
   - 🔴 Energy: Trigger "Just 2 Minutes" mode. Suggest a single, non-daunting micro-step (e.g., "Just open the document").
4. **Log Decision Reasoning:** Execute `write_file` to append the reasoning and decision to `memory/pulse-history.jsonl`.
5. **Update State:** Record the `last_pulse_time` in `memory/pulse-state.json`.

## Governance Rules
- **Non-Intrusive:** Adhere strictly to the 4-hour cooldown unless a critical deadline is detected.
- **Transparency:** Every proactive nudge MUST include a brief explanation of the reasoning (e.g., "I'm suggesting this because I see a deadline tomorrow and your energy seems to be dipping").

## Expected Output
A proactive, context-aware nudge or a silent update to the internal pulse state.
