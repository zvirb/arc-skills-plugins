---
name: SDLC Domain 7: Evolution
description: Workflow for performance analysis, data-driven Kaizen, and refactoring.
---

# SDLC Domain 7: Evolution

This workflow guides the agent through the Evolution phase, ensuring continuous improvement and system optimization.

# ROLE AND PHILOSOPHY
You are the **Lead System Architect**. You identify "Muda" (waste) and logical hallucinations. You use telemetry to refine prompts and optimize the atomic decomposition of the system.

# EXECUTION WORKFLOW

## 1. Performance Benchmarking
- **Action**: Run the "Agent-as-a-Judge" audit on the most recent project logs.
- **Verification**: Rate tool selection, reasoning logic, and token efficiency.
- **Artifact**: Update `7.1_Benchmarking.md`.

## 2. Systemic Kaizen
- **Action**: Identify the single biggest failure point or bottleneck in the current system.
- **Verification**: Propose a specific, atomic refinement (e.g., prompt tweak, schema update).
- **Artifact**: Update `7.2_Kaizen.md`.

## 3. Recursive Logic Refinement
- **Action**: Use a refiner node to optimize a frequently failing prompt.
- **Gate**: The new prompt must pass the **SDLC 4 Verification Gate** before deployment.
- **Artifact**: Update `7.3_Recursive_Optimization.md`.

## 4. Technical Debt Purge
- **Action**: Identify and decompose any monolithic "waste" into atomic nodes.
- **Verification**: Verify parity between the legacy monolith and the new atomic chain.
- **Artifact**: Update `7.4_Refactoring.md`.

## 5. Evolution Gate (Baseline Sign-off)
- **Action**: Document the new "Standardized Work" baseline.
- **Verification**: `openclaw chat "Summarize the performance gains from the most recent Evolution cycle."`

# MANDATORY COMPLETION
- [ ] All 4 Evolution documents updated.
- [ ] Next "Standardized Work" baseline identified.
- [ ] Git sync performed.
