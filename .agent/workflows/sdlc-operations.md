---
name: SDLC Domain 6: Operations
description: Workflow for observability, telemetry, and VRAM/KV cache management.
---

# SDLC Domain 6: Operations

This workflow guides the agent through operational monitoring and health checks of the OpenClaw swarm.

# ROLE AND PHILOSOPHY
You are the **Lead System Auditor**. You monitor for resource contention and behavioral drift. You use data-driven insights to recommend optimizations for the Maxwell/Pascal topology.

# EXECUTION WORKFLOW

## 1. Physical Health Check
- **Action**: Execute `nvidia-smi` and parse VRAM/Temperature data.
- **Verification**: Ensure Pascal (GPU 0) and Maxwell (GPU 1) are within target utilization bands.
- **Artifact**: Log results to `6.1_Infrastructure_Monitoring.md`.

## 2. Decision Path Analysis
- **Action**: Retrieve and analyze the trace of the most recent agent session.
- **Verification**: Check for redundant loops or "Context Bloat".
- **Artifact**: Update `6.2_Agentic_Telemetry.md`.

## 3. KV Cache Optimization
- **Action**: Audit the context window settings in `openclaw.json`.
- **Verification**: Ensure worker nodes are capped at 4k tokens and **Q8_0 quantization** is active for the cache.
- **Artifact**: Update `6.3_KV_Cache.md`.

## 4. Maintenance & Cleanup
- **Action**: Execute automated cleanup scripts for stale logs and memory.
- **Command**: `openclaw chat "Clean up stale memory files in /Memory/core"` (if summarizer skill exists).
- **Artifact**: Update `6.4_Maintenance.md`.

## 5. Operations Gate (Health Sign-off)
- **Action**: Confirm that all "Andon" alerts are resolved.
- **Verification**: `openclaw chat "Check vitals.log for unresolved OOM or drift alerts."`

# MANDATORY COMPLETION
- [ ] All 4 Operations documents updated with current telemetry.
- [ ] System vitals verified as healthy.
- [ ] Git sync performed.
