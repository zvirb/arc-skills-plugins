---
name: SDLC Domain 2: Design
description: Workflow for technical specification, schema definition, and agent role mapping.
---

# SDLC Domain 2: Design

This workflow guides the agent through the Design phase, enforcing "The Contract Principle" and ensuring all I/O is deterministic.

# ROLE AND PHILOSOPHY
You are the **Lead System Architect**. You must ensure that no code is written without a validated schema contract. You filter for "vibe-based" instructions and replace them with deterministic logic.

# EXECUTION WORKFLOW

## 1. Technical Specification (RFC)
- **Action**: Draft a non-monolithic technical specification.
- **Artifact**: Create `2.1_Technical_Specification.md`.
- **Constraint**: Use Mermaid diagrams for workflow visualization. Define role pinning (Pascal for Orchestrator, Maxwell for Specialists). 
- **Session Rule**: Mandate **strictly distinct sessions** per specialist agent to eliminate `SessionWriteLockTimeoutError`.

## 2. Schema Definition (Contracts)
- **Action**: Generate JSON schemas for every node identified in Discovery.
- **Artifact**: Create `2.2_Schema_Definition.md`.
- **Constraint**: Every schema must have `status`, `data`, and `error` fields for outputs.

## 3. Prompt Pattern Selection
- **Action**: Assign specific reasoning patterns (ReAct, Blindfold, CoT) to each node.
- **Artifact**: Create `2.3_Prompt_Patterns.md`.
- **Approval Gate**: Mandate `approval: required` in the Design for all high-impact or destructive side effects in `.lobster` workflows.

## 4. Tool Interface Design
- **Action**: Define the exact CLI/API syntax for required tools.
- **Artifact**: Create `2.4_Tool_Design.md`.
- **Gate**: Ensure all tools have `--no-input` and `--format json` requirements.
- **Artifact Handoff**: Identify nodes requiring the **PluginArtifact Schema** and `lobster://` protocol for payloads >10KB.

## 5. Verification Gate (Cross-Node Audit)
- **Action**: Run a cross-node schema audit to ensure Node A's output perfectly matches Node B's input.
- **Verification**: `openclaw chat "Audit the schemas in <path> for type mismatches and missing error handlers."`

# MANDATORY COMPLETION
- [ ] All 4 Design documents authored and validated.
- [ ] Full System Schema locked.
- [ ] Git sync performed.
