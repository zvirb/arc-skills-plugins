# Configuration Context

This folder contains non-secret configuration files (e.g., `agents.yaml`, `prompts/`). All configuration must adhere to the **May 2026 Infrastructure Standards (v2026.5.x)**.

## 1. Model Routing Standards
Routing rules must account for hardware constraints:
*   **Pascal P100 (24GB):** Default for `Qwen 3.6 35B-A3B`. Handles all multi-step orchestration.
*   **Maxwell M40 (12GB):** Restricted to `DeepSeek-OCR 2` and `Qwen 2.5 Coder (7B)`.
*   **Pinning:** All routing MUST use explicit API endpoints pinned to specific GPUs to avoid PCIe bus contention.

## 2. Global Operational Limits
Config files governing the gateway (e.g., `openclaw.json`) MUST enforce:
*   `imageMaxDimensionPx: 800` (Vision circuit breaker).
*   `OLLAMA_NUM_CTX: 4096` (Context ceiling).
*   `gateway.reload.mode: "hybrid"` (Safe hot-reloading).

## 3. Redaction Lockout (CRITICAL)
NEVER allow an agent to read `openclaw.json` or any file containing `***` redacted placeholders and then write it back to disk. This will permanently erase functional API keys. Use the `OPENCLAW_CONFIG_PATH` environment variable for mutable config overrides.

## 4. Rule
DO NOT put API keys, tokens, or PII in this folder. All sensitive data MUST be stored in `Secrets/`.
