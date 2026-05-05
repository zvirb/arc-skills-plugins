# OpenClaw SDLC Architecture Framework

## Overview
This directory contains the deterministic, modular Software Development Life Cycle (SDLC) framework for the OpenClaw multi-agent ecosystem. This framework is built on the principles of **Lean Manufacturing**:
- **Kaizen (改善):** Continuous improvement through atomic breakdown.
- **Standardized Work (標準作業):** Simplifying tasks to their absolute core.
- **Jidoka (自働化):** Autonomation and self-healing validation loops.

## SDLC Domains
The lifecycle is partitioned into seven discrete cognitive domains, each containing granular, non-monolithic documentation and automated workflows.

1.  **[Discovery](./Discovery/README.md)**: Problem framing, requirement gathering, and atomic decomposition.
2.  **[Design](./Design/README.md)**: Technical specification, schema definition, and agent role mapping.
3.  **[Implementation](./Implementation/README.md)**: Atomic node construction, prompt engineering, and tool binding.
4.  **[Verification](./Verification/README.md)**: Deterministic evaluation, Jidoka loops, and state-change confirmation.
5.  **[Delivery](./Delivery/README.md)**: Deployment, plugin compilation, and agent binding.
6.  **[Operations](./Operations/README.md)**: Observability, telemetry, and VRAM/KV cache management.
7.  **[Evolution](./Evolution/README.md)**: Performance analysis, data-driven Kaizen, and refactoring.

## Core Architectural Principles (v2026.5.x)
- **Deterministic Orchestration**: Use **Lobster** macros over probabilistic tool loops.
- **Hardware Specialization**: Pin models strictly to **Pascal** (Orchestration) or **Maxwell** (Workers).
- **Zero Trust Configuration**: No automated writes to `openclaw.json` to prevent redaction and symlink damage.
- **Memory Efficiency**: Enforce **INT4** quantization, **Q8_0** KV caching, and strict **4k context** worker caps.
- **Asynchronous Stability**: Enable **Heavy Task Offload** to preserve gateway event loop fluidity.
- **Grounding over Guessing**: Success is defined only by valid, schema-compliant data, never by LLM text.
