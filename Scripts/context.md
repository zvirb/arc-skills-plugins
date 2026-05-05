# Scripts Context

This folder contains utility scripts and automations. All scripts must adhere to the **May 2026 Infrastructure Standards (v2026.5.x)** for deterministic, autonomous execution.

## 1. Deterministic Execution (Jidoka)
*   **Non-Interactive:** All scripts MUST include `--force`, `--no-input`, or equivalent flags to prevent execution hangs in background workflows.
*   **Schema-Driven:** Use structured JSON for inputs/outputs to ensure rigid mapping and prevent tool-calling hallucinations.
*   **Self-Healing:** Implement retry loops with exponential backoff for network-dependent scripts (e.g., Google Workspace API calls).

## 2. Environment Parity
*   **SSH Isolation:** Scripts designed for testing or deployment MUST be validated via SSH on **alienware**. 
*   **Path Safety:** Use absolute paths where possible to avoid context-dependent failures (Bug #68101).
*   **Redaction Awareness:** Scripts that parse `openclaw.json` must handle the `***` redaction string gracefully to avoid corrupting configuration.

## 3. Guidelines
1. **Global Utilities:** Scripts here should serve the project as a whole.
2. **Atomic Scope:** Prefer many small, single-responsibility scripts over one monolithic script.
3. **Validation:** Every script should have a corresponding verification step or command to confirm successful execution.
