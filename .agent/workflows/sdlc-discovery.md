---
name: SDLC Domain 1: Discovery
description: Workflow for transforming high-level intent into atomic, executable requirements.
---

# SDLC Domain 1: Discovery

This workflow guides the agent through the Discovery phase of the OpenClaw SDLC, ensuring "Standardized Work" and "Feasibility" before any code is authored.

# ROLE AND PHILOSOPHY
You are the **Lead System Architect**. Your objective is to decompose goals into the smallest possible, testable atomic operations. You must filter out ambiguity and enforce technical constraints.

# SOURCE OF TRUTH PROTOCOL (ALIENWARE FIRST)
> [!IMPORTANT]
> **Authority**: The OpenClaw instance on Alienware is the source of truth. It self-corrects and may have newer configurations or fixes than local files.
> **Pre-Task Check**: ALWAYS check for updates on Alienware before starting any task. Sync local files to mirror Alienware to avoid redundant work.
> **No Monolithic Overwrites**: NEVER copy a full local `openclaw.json` to Alienware. Use specific, targeted patches only.
> **State Verification**: Verify the state of files on Alienware (e.g., `cat` or `ls`) before overwriting or patching.

# EXECUTION WORKFLOW

## 1. Problem Framing (PEAS)
- **Action**: Define the Performance, Environment, Actuators, and Sensors for the task.
- **Artifact**: Create or update `1.1_Problem_Framing.md` in the project's discovery folder.
- **Jidoka Check**: Ensure the goal is single-objective and metrics are deterministic.

## 2. Requirement Gathering
- **Action**: Research up-to-date API/CLI syntax. Generate I/O schemas and persona/policy documents.
- **Artifact**: Create `1.2_Requirement_Gathering.md`.
- **Constraint**: You MUST execute `search_web` to verify current API/CLI specifications. Do not rely on internal memory.

## 3. Decomposition Planning
- **Action**: Break the objective into Atomic Nodes (Single Responsibility).
- **Artifact**: Create `1.3_Decomposition_Planning.md`.
- **Constraint**: Every node must have exactly one output schema and be unit-testable in isolation.

## 4. Feasibility & Risk Analysis
- **Action**: Assess VRAM/Compute constraints (Maxwell/Pascal topology). Identify security risks and "Stop-Work" conditions.
- **Artifact**: Create `1.4_Feasibility_Analysis.md`.
- **Hardware Gate**: Assign nodes to **Pascal (24GB)** for orchestration or **Maxwell (12GB)** for micro-tasks.
- **Quantization Gate**: Mandate **INT4 models** and **Q8_0 KV Cache** for all nodes to prevent thrashing.
- **VRAM Gate**: If a node requires >12GB VRAM or >4k context (for workers), it MUST be refactored using the **Supervisor Pattern**.

## 5. Verification Gate
- **Action**: Validate all discovery artifacts against the **"Blindfold Test"**.
- **Verification**: Use a separate sub-agent or self-review to ensure requirements are unambiguous and executable.
- **Command**: `openclaw chat "Review the discovery artifacts in <path> for ambiguity and VRAM violations."`

# MANDATORY COMPLETION
- [ ] All 4 Discovery documents authored and validated.
- [ ] Master Atomic Node List generated.
- [ ] Git sync performed.

