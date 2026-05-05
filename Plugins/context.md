# Open Claw Plugins Context

This folder contains Plugins for Open Claw. All development must adhere to the **May 2026 Infrastructure Standards (v2026.5.x)** to ensure stability on heterogeneous legacy hardware.

## 1. Hardware-Aware Model Specialization
To maintain a resilient swarm on the Pascal/Maxwell cluster, plugins must target specific models based on their role:
*   **Orchestrator (Pascal 24GB):** `Qwen 3.6 35B-A3B (INT4)`. Use for multi-turn reasoning and supervisor routing.
*   **Vision Specialist (Maxwell 12GB):** `DeepSeek-OCR 2`. Mandatory for layout analysis and technical drawings.
*   **Micro-Agent Swarm (Maxwell 12GB):** `Qwen 2.5 Coder (7B)`. High-speed, isolated data extraction.

## 2. Infrastructure & VRAM Protection
*   **KV Cache Management:** All local models MUST use `OLLAMA_KV_CACHE_TYPE=q8_0` and be restricted to `OLLAMA_NUM_CTX=4096` to prevent OOM and PCIe bottlenecks.
*   **Payload Scaling:** Set `imageMaxDimensionPx: 800` in `openclaw.json` as a VRAM circuit breaker.
*   **Complete Instance Isolation:** Pin models to specific GPUs via `CUDA_VISIBLE_DEVICES`. Do NOT attempt Tensor Parallelism across PCIe 3.0.

## 3. Concurrency & State Standards
*   **Lean Architecture:** Specialists must operate in **Isolated Sessions** (`--session isolated`). Avoid sharing session IDs to prevent `SessionWriteLockTimeoutError`.
*   **Bypassing 10KB Limits:** For heavy payload handoffs, use the `lobster://` blob protocol and `PluginArtifact` metadata schema instead of raw JSON-RPC string passing.
*   **Persistent State:** Use the native SDK storage handlers (`api.storage.get()` / `api.storage.set()`) to manage state. Do NOT use the LLM context window as a database.

## 4. Development Rules & Structure
1. **Sub-Folder Isolation:** Every new plugin MUST be created in its own dedicated sub-folder.
2. **Compilation Requirement:** Since plugins are written in TypeScript, you MUST compile them (`npm run build`) before installation. Ensure the entry point in `package.json` points to the compiled JavaScript (`dist/`).
3. **Plugin Manifests:** Every plugin MUST include a `contracts` block in `openclaw.plugin.json` declaring its tools. This prevents "non-capability" classification.
4. **Mandatory Testing:** All testing MUST occur via SSH on **alienware**. Local WSL testing is strictly forbidden. 
5. **Physical Verification:** For state-mutating actions, use the `browser` tool to verify the change in the user's workspace.

## 5. Plugin Antipatterns & SDK Best Practices
1. **The Sub-Shell Orchestration Anti-pattern:** Forbidden to use `child_process.exec` to call `openclaw` or `gog`. Use native SDK bindings (e.g., `api.infer(prompt)`).
2. **Unvalidated Environment Variables:** Forbidden to read `process.env` dynamically. Export a `configSchema` (Zod) in `IPlugin`.
3. **Path Traversal & Unsafe State Persistence:** Forbidden to hardcode relative escape paths (e.g., `../../../../Memory/`). Use `api.storage`.
4. **Redaction Lockout:** Never allow an agent to read/write `openclaw.json` directly. Overwriting functional keys with `***` redaction strings is a terminal failure.

## 6. Integration Status
* **GOG Integration:** Re-authorized via SSH-tunneled OAuth. `gog calendar` and `gog tasks` are confirmed operational. If `invalid_grant` errors recur, repeat the SSH-tunneled OAuth flow.

## 7. GOG CLI Defensive Engineering (May 2026 Standard)
All plugins that invoke the `gog` CLI via `child_process` (or via `exec` wrapper tools) MUST follow these hardened patterns:
*   **Double-Dash Protocol:** Every `gog` command MUST use `--` before any positional text argument: `gog tasks create -- "Title"`. This prevents leading hyphens in LLM output from being parsed as flags.
*   **Schema-Based Parameter Builder:** NEVER concatenate raw LLM text into a CLI string. Build a sanitized argument map from structured JSON fields, then assemble the CLI call programmatically.
*   **Bullet/Unicode Stripping:** Strip `•`, `-`, `*`, `·` from all LLM-generated text values before CLI construction.
*   **Whitespace Quoting:** Always double-quote multi-word args. Unquoted whitespace causes silent argument-splitting failures.
*   **JSON Validation Gate:** Use `gog ... --json` and parse the result. Validate that `title`, `id`, and status fields match expected values. On mismatch, throw a structured error to trigger the Andon retry loop.
*   **`--force` / `--no-input`:** Append to all non-interactive invocations to prevent headless execution hangs.
*   **Reference:** `Docs/20260505/Agentic Workflow Defensive Engineering Guide.md` and `Docs/20260505/Google Workspace CLI Workflow Integration.md`.
