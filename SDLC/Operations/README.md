# SDLC Domain 6: Operations

## Purpose
The Operations domain focuses on the "Observability" and "Maintenance" of the active agent swarm. This phase ensures that infrastructure resources (VRAM, KV Cache) and agentic behaviors (Decision Paths, Tool I/O) are monitored and optimized for long-term sustainability.

## Documents
- **[6.1 Infrastructure Monitoring](./6.1_Infrastructure_Monitoring.md)**: Tracking VRAM, GPU utilization, and PCIe bandwidth.
- **[6.2 Agentic Telemetry](./6.2_Agentic_Telemetry.md)**: Tracing decision paths, tool I/O, and prompt tokens.
- **[6.3 KV Cache Management](./6.3_KV_Cache.md)**: Optimizing memory usage and preventing OOM failures.
- **[6.4 Maintenance & Drifts](./6.4_Maintenance.md)**: Detecting behavioral drift and performing system updates.

## Workflows
- `ops-monitor`: Real-time health check of the Maxwell/Pascal topology.
- `ops-trace`: Analyze the decision trace of a specific agent session.
- `ops-cleanup`: Automated cleanup of stale `Memory/` and `Logs/`.

## Jidoka Gate
The Operations phase is active continuously. The **System Vital Monitor** must trigger an automated "Andon" alert if VRAM utilization exceeds 95% or if the average "Decision Confidence" score drops below the defined threshold.
