---
name: SDLC Domain 3: Implementation
description: Workflow for atomic node construction, prompt engineering, and tool binding.
---

# SDLC Domain 3: Implementation

This workflow guides the agent through the Implementation phase, ensuring "Standardized Work" and "Least Privilege" execution.

# ROLE AND PHILOSOPHY
You are the **Lead System Architect**. You build atomic, single-responsibility components. You strictly avoid monolithic scripts and aggregate tool calls.

# EXECUTION WORKFLOW

## 1. Environment Verification
- **Action**: Verify required binaries and secrets exist in `Secrets/` or the system path.
- **Constraint**: Execute `which <tool>` or `<tool> --help` before writing any code.
- **Performance Check**: Ensure `heavy_task_offload_enabled: true` is active in `openclaw.json` for stable tool initialization.

## 2. Component Scaffolding
- **Action**: Create the directory structure in `Skills/` or `Plugins/`.
- **Artifact**: Generate `SKILL.md` (Skills) or `package.json`/`index.ts` (Plugins).

## 3. Atomic Node Implementation
- **Action**: Implement the logic and prompts defined in the Design phase.
- **Artifact**: Create `3.1_Atomic_Nodes.md`.
- **Constraint**: Configure nodes for **INT4 quantization** and **Q8_0 KV Cache**.
- **Jidoka Check**: Include `try-catch` blocks and schema validation loops.

## 4. Local Unit Testing
- **Action**: Test the component in isolation.
- **Mandatory**: Testing MUST occur via **SSH on Alienware**. Local WSL testing is forbidden.
- **Verification (Skills)**: `openclaw skills check <slug>`.
- **Verification (Plugins)**: `npm run build && openclaw plugins list --verbose`.

## 5. Verification Gate (Blindfold Test)
- **Action**: Run the node through `openclaw chat` with the "Blindfold Prompt".
- **Verification**: Ensure the node maps input to output without any conversational hallucination.

# MANDATORY COMPLETION
- [ ] All components implemented and unit-tested.
- [ ] No monolithic scripts present.
- [ ] Git sync performed.
