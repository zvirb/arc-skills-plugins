# OpenClaw Extensions: Best Practices & Common Issues

This document aggregates deep research into the architecture of OpenClaw Plugins (TypeScript) and Skills (Markdown), specifically detailing the most common issues developers encounter and the architectural patterns required to solve them.

---

## 1. Context Bloat (The "Firehose" Anti-Pattern)
**The Issue:**
A common mistake when building data-fetching plugins (e.g., retrieving emails, searching databases) is returning the entire raw JSON payload to the OpenClaw agent. This blows up the context window, drastically increases token costs, and severely degrades the LLM's reasoning capability.
**The Solution (Standardized Work):**
- Plugins must implement strict pagination (`limit` and `offset` parameters in the `configSchema`).
- Before returning data to the agent, the Plugin should truncate or project the data (returning only essential fields like `id`, `title`, `status`), stripping out raw HTML or massive text blocks.
- For large documents, the Plugin should route the raw data to a specialized `llm_extract_json` or `llm_summarize_text` native API internally, returning only the synthesized summary to the active agent.

## 2. Silent Validation Failures (The "Jidoka" Breach)
**The Issue:**
Developers often write plugins that assume the LLM will provide perfectly formatted arguments. When the LLM hallucinates a parameter (e.g., passing a string instead of an array), the plugin crashes, and the agent's workflow halts abruptly without explanation.
**The Solution (Self-Healing Loops):**
- Every plugin tool MUST wrap its execution in a `try/catch` block.
- Errors must never bubble up to crash the OpenClaw runtime. Instead, catch the error and return a structured JSON response: `{ "success": false, "error": "Invalid argument: expected Array, got String. Please correct and retry." }`.
- This enables the OpenClaw agent to read the error and correct its own prompt (the "Andon Loop").

## 3. Zombie Subshells & Concurrency Leaks
**The Issue:**
Wrapping native CLI binaries (like `gog` or `curl`) via `child_process.exec` inside a TypeScript plugin. In highly concurrent agent workflows, these sub-shells can hang indefinitely if they require interactive prompts (e.g., OAuth flows), spawning zombie processes that eventually crash the WSL/Node host.
**The Solution:**
- Strictly use native Node.js SDKs (e.g., `composio-core`, `axios`, native `@openclaw/plugin-sdk` `api.infer`) instead of `wsl bash -c`.
- If a binary execution is absolutely unavoidable, developers MUST implement strict timeouts (e.g., `execAsync(cmd, { timeout: 5000 })`) and capture `stderr`.

## 4. Manifest Dependency Collisions
**The Issue:**
Developers build monolithic workflow plugins (e.g., `AutonomousWorkflows`) that dynamically call tools from other plugins via `api.executeTool('some_other_tool')`. If the target plugin fails to load (due to a missing API key), the workflow plugin crashes at runtime.
**The Solution:**
- Explicit Dependency Declaration: Plugins must export a `manifest` object detailing an array of `dependencies: ["target-plugin"]`. The OpenClaw engine resolves this Directed Acyclic Graph (DAG) at boot, refusing to load the workflow if its dependencies are unsatisfied.

## 5. Cognitive Drift in Markdown Skills
**The Issue:**
Writing `SKILL.md` files as conversational or overly verbose stories. The LLM loses track of the strict trigger conditions and begins executing tools arbitrarily.
**The Solution (Kaizen Prompts):**
- Skills must be brutally concise. Use strict YAML frontmatter (`requires: bins: []`).
- Use algorithmic formatting for instructions:
  `WHEN [Condition] THEN [Execute tool_x with Schema Y]`.
- Do not provide code examples in Python. Provide JSON argument examples for the target Plugin tools.

## 6. Unsafe Path Traversal
**The Issue:**
Plugins attempting to manage their own state by hardcoding relative filesystem paths (e.g., `fs.writeFileSync('../../../Memory/state.json')`). This breaks sandboxing and fails across different operating systems.
**The Solution:**
- Exclusively use the native SDK storage handlers: `api.storage.get('key')` and `api.storage.set('key', value)`. The host engine determines where and how to persist this securely.

## 7. Ghost Skills (The Registration Breach)
**The Issue:**
Developers install a new skill via `openclaw skills install <path>` (which correctly registers it in the `skills.entries` registry) but find that the agent is completely unaware of the skill and refuses to use it.
**The Solution:**
- In the OpenClaw architecture, skills are not automatically inherited by agents.
- **CRITICAL DEPLOYMENT STEP:** You MUST manually bind the new skill's slug to the target agent in `openclaw.json`. 
- Locate the `agents.list` array, find your specific agent profile (e.g., `"id": "main"`), and append the skill to its `"skills": []` array.
- Restart the `openclaw-gateway` service. Failure to explicitly bind the skill will result in a "Ghost Skill" that the engine loads but the agent cannot see.

## 8. The CLI Hallucination Trap (Execution Missing)
**The Issue:**
Developers create Markdown skills (`SKILL.md`) with instructions like "Execute the native terminal command `gog tasks list`", assuming the LLM has a native `bash` or `shell` tool to run it. If no such generic execution tool exists, the LLM assumes `gog` is the literal name of a tool and hallucinates a tool call to `"name": "gog"`. The engine immediately rejects this with "Tool gog not found", breaking the workflow.
**The Solution:**
- Markdown Skills ONLY inject text into the agent's system prompt; they DO NOT magically create tools or grant terminal access.
- If a skill workflow relies on a native CLI binary (like `gog` or `curl`), you MUST accompany it with a TypeScript Plugin that explicitly registers that binary as a tool (e.g., `api.registerTool('gog')`).
- The Plugin must securely wrap the execution using `child_process.execAsync(cmd, { timeout: 10000 })` to ensure the agent has a valid target tool in its schema to invoke.

## 9. Lack of Empirical Verification
**The Issue:**
Relying solely on CLI return codes or "Success" text from an LLM. Tools may return 0 (success) but fail to actually persist data in the target system (e.g., a silent API error or token mismatch).
**The Solution (Independent Browser Verification):**
- For all Google Workspace interactions, the developer MUST use the `browser` tool to navigate to the live service (Gmail, Tasks, Calendar) and confirm the mutation.
- This is a non-negotiable step in the "Trust But Verify" protocol.

## 10. API Schema Hallucination
**The Issue:**
Assuming an API's schema or a tool's flags based on outdated training data.
**The Solution (Extensive Research):**
- Before implementing any tool interaction, you MUST perform a mandatory online research step to retrieve the latest documentation, schemas, and required parameters for the target service.
## 11. The Monolithic Binding Trap (KV Cache Exhaustion)
**The Issue:**
Binding all 50+ available skills to a single agent profile in `openclaw.json`. This forces the OpenClaw gateway to inject the JSON schemas for every single tool into every prompt, exhausting the KV cache (context window) and causing "context runout" on legacy hardware (Pascal/Maxwell).
**The Solution (Standardized Lean Architecture):**
- **Quantization:** Enforce **INT4 models** and **Q8_0 KV Cache** to reduce VRAM pressure.
- **Context Limits:** Capped at **4k tokens** for worker nodes to prevent reasoning degradation.
- **Deterministic Workflows:** Instead of probabilistic `load_skill` loops, use **.lobster macros** with **Static Deterministic Binding** (`tools.alsoAllow`). This ensures tools are available exactly when needed without bloating the persistent agent context.

## 12. The Routing Index Bottleneck (Discovery Failure)
**The Issue:**
In a progressive disclosure model, the `root-router` can fail if it doesn't know what a sub-skill is called or what it does. Hardcoding the list of skills into the router's prompt is brittle and leads to maintenance debt.
**The Solution (Dynamic Manifests):**
- Maintain a `MANIFEST.md` in the `skills/` directory that is automatically generated from skill frontmatter (name and description).
- Instruct the `root-router` to call `read("skills/MANIFEST.md")` as its first step if it cannot find a matching skill for the user's intent. This ensures the router has an up-to-date "map" of the entire library without bloating its system prompt.

## 13. Jidoka Shell Wrappers (Failure Masking)
**The Issue:**
Calling CLI tools directly from a skill (e.g., `bash run.sh`) often results in raw shell errors (exit code 1, stderr) that the agent interprets as a tool-use failure rather than a domain-level error. This prevents the agent from analyzing the failure and correcting itself.
**The Solution (Structured JSON Results):**
- Wrap all CLI calls in a hardened script (e.g., `scripts/run.sh`) that captures errors and returns a deterministic, structured JSON payload: `{ "STATUS": "ERROR", "EXIT_CODE": 1, "ERROR_MSG": "..." }`.
- This transforms "Shell Failures" into "Data Results" that the agent can reason about, enabling autonomous self-healing and smarter retries.

## 14. Remote Config Corruption (Service Overwrites)
**The Issue:**
When manually editing `openclaw.json` on a remote node while the `openclaw-gateway` service is running. On exit or restart, the service may flush its in-memory state back to the disk, overwriting manual edits and causing "config reversion".
**The Solution (Safe Persistence):**
- **STOP FIRST:** Always stop the `openclaw-gateway` service (e.g., `systemctl --user stop openclaw-gateway`) BEFORE attempting to modify the `openclaw.json` or `.env` files.
- **UPLOAD & START:** Push the updated files and then start the service. This ensures the engine loads the new state cleanly without a collision during the shutdown phase.

## 16. The GitOps Symlink Trap (Atomic Write Failure)
**The Issue:**
In GitOps environments, configuration files are often symlinks to a versioned directory. Atomic writes (like those from `openclaw skills install`) will break the symlink and fail to propagate to the real config, or the engine will continue reading the stale symlink.
**The Solution:**
- **Explicit Paths:** Always use `OPENCLAW_CONFIG_PATH` to point directly to the physical file.
- **Atomic Preflights:** Forbid configuration mutation during the "Warmup" phase of the gateway.

## 17. Session Lock Contention (State Deadlock)
**The Issue:**
Multiple specialist agents attempting to write to the same session simultaneously, triggering `SessionWriteLockTimeoutError`.
**The Solution:**
- **Isolated Sessions:** Every specialist in a `.lobster` pipeline MUST execute in its own **strictly distinct session ID**.
- **Lease-based Locking:** Implement short TTL leases for shared state files.

## 18. JSON-RPC Payload Limits (Context Overflow)
**The Issue:**
Attempting to pass large binary or text artifacts (>10KB) as string parameters in tool calls. This causes JSON-RPC serialization errors and context saturation.
**The Solution:**
- **Artifact Handoff:** Use the **PluginArtifact Schema** and the **lobster://** protocol to pass data by reference (blob storage) rather than by value.

## 19. PCIe 3.0 Bottlenecks (Latency Fragmentation)
**The Issue:**
Loading large models across multiple GPUs on legacy boards (Pascal/Maxwell), forcing heavy data transfer over slow PCIe 3.0 lanes.
**The Solution:**
- **GPU Pinning:** Pin specific roles to specific GPUs (e.g., Orchestrator on Pascal, Vision/Workers on Maxwell) to keep inference local to the VRAM. Disable Tensor Parallelism on legacy hardware.
