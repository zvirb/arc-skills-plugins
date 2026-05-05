# Logs Context

This folder contains execution traces, error logs, and debug outputs. All telemetry must adhere to the **May 2026 Infrastructure Standards (v2026.5.x)** for reliable multi-agent auditing.

## 1. Forensic Debugging & Observability
*   **The TUI (Preferred):** Use `openclaw tui` (press `[L]`) to observe step-by-step tool execution and session transitions in real-time.
*   **Leveling:** Default to `--log-level info`. Use `debug` only for isolated investigation of `SessionWriteLockTimeoutError` or PCIe bottlenecking.
*   **Deterministic Normalization:** Logs should be structured as JSON where possible to allow for automated analysis of agent performance.

## 2. Resource Exhaustion Triggers
Monitor logs for the following hardware-specific warnings:
*   `OOM` / `CUDA Error`: Indicates `imageMaxDimensionPx` or `OLLAMA_NUM_CTX` limits were exceeded.
*   `PCIe Timeout`: Indicates model contention on the same GPU; verify `CUDA_VISIBLE_DEVICES` pinning.

## 3. Note
This entire directory is ignored by Git. It is safe to dump verbose telemetry here for forensic analysis.
