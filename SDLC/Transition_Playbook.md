# OpenClaw SDLC Transition Playbook

## Overview
This playbook defines the standardized procedures for transitioning between SDLC domains. Each transition is protected by a **Jidoka Gate** requiring independent, schema-based confirmation.

## 1. Discovery → Design
- **Trigger**: Problem framed and atomic decomposition planned.
- **Verification**: 
    - [ ] PEAS model defined and documented.
    - [ ] Master Atomic Node List generated.
- **Gatekeeper**: Lead System Architect.
- **Action**: `sdlc-design-spec` workflow.

## 2. Design → Implementation
- **Trigger**: System schemas locked and role pinning defined.
- **Verification**: 
    - [ ] Every node has a validated I/O schema.
    - [ ] Maxwell/Pascal resource allocation confirmed.
- **Gatekeeper**: Lead System Architect.
- **Action**: `sdlc-impl-node` or `sdlc-impl-plugin` workflow.

## 3. Implementation → Verification
- **Trigger**: Code/Skill authored and .lobster macro defined.
- **Verification**: 
    - [ ] Blindfold Test passed (no conversational hallucination).
    - [ ] Plugin/Skill survives the load pipeline.
    - [ ] Specialist agents utilize strictly distinct isolated sessions.
    - [ ] Data handoffs use PluginArtifact schema/lobster:// protocol.
- **Gatekeeper**: Lead System Auditor.
- **Action**: `sdlc-verify-node` workflow.

## 4. Verification → Delivery
- **Trigger**: Independent auditor sign-off and state confirmation.
- **Verification**: 
    - [ ] Physical state change verified via `browser` or `curl`.
    - [ ] No tools used to "fix" state during audit.
- **Gatekeeper**: Lead System Auditor.
- **Action**: `sdlc-delivery-deploy` workflow.

## 5. Delivery → Operations
- **Trigger**: Heartbeat task successful and Git sync performed.
- **Verification**: 
    - [ ] `openclaw.json` matches Git source of truth.
    - [ ] Vitals (VRAM/Temp) within target bands.
- **Gatekeeper**: Lead System Auditor.
- **Action**: `sdlc-ops-monitor` workflow.

## 6. Operations → Evolution
- **Trigger**: Sufficient telemetry collected (min 10 sessions).
- **Verification**: 
    - [ ] Behavioral drift or VRAM bottlenecks identified.
    - [ ] Performance Lift metrics baseline defined.
- **Gatekeeper**: Lead System Architect.
- **Action**: `sdlc-evo-bench` workflow.

## 7. Evolution → Discovery (The Kaizen Loop)
- **Trigger**: Next Standardized Work baseline identified.
- **Verification**: 
    - [ ] Refactoring requirements drafted.
    - [ ] Performance improvement demonstrated.
- **Gatekeeper**: Lead System Architect.
- **Action**: Restart Discovery for the next iteration.
