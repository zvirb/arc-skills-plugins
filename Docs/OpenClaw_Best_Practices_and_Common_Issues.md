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
