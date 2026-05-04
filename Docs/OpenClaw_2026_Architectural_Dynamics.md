# Architectural Dynamics and Registry Optimization in the OpenClaw 2026.5.x AgentRuntime

The evolution of OpenClaw from its foundational roots as Clawdbot and Moltbot into a sophisticated, multi-tenant autonomous agent runtime has necessitated a fundamental re-engineering of the plugin architecture. In the 2026.5.x release cycle, the framework has transitioned toward an aggressively decoupled design where core gateway logic is strictly isolated from vendor-specific capabilities. 

This architectural shift is most visible in the AgentRuntime toolset, which now acts as the central orchestrator for a growing ecosystem of over 80 extensions and hundreds of specialized skills. For a plugin to integrate dynamic tools such as load_skill and execute_skill without being marginalized by the registry’s "non-capability" classification, developers must adhere to a rigid manifest schema and registration protocol that satisfies both the control-plane discovery and the runtime execution layers.

## The Evolution of Plugin Lifecycle and Discovery

The current version of OpenClaw (2026.5.x) operates on a four-tier discovery priority system that dictates how code is loaded into the gateway process. The order of precedence ensures that local workspace overrides always supersede global or bundled defaults, a design choice that facilitates rapid iterative development of custom skills and tools.

| Priority | Source Tier | Discovery Path | Use Case |
| :--- | :--- | :--- | :--- |
| 1 | plugins.load.paths | Explicit configuration in openclaw.json | Custom enterprise plugins or absolute local paths |
| 2 | Workspace Plugins | <workspace>/.openclaw/ | Project-specific agent enhancements |
| 3 | Global Plugins | ~/.openclaw/ | User-wide persistent tools and memory backends |
| 4 | Bundled Plugins | dist/extensions/ | Official model providers, speech, and core utilities |

This precedence model is critical when registering dynamic tools like load_skill because the AgentRuntime rebuilds its tool list at the start of every agent turn. The gateway scans for native plugins—defined by the presence of an openclaw.plugin.json manifest—before engaging in "capability discovery". If a plugin is misplaced in the directory hierarchy or lacks a valid manifest, the openclaw doctor utility will flag it as a "stale alias" or an "inert reference," preventing the tools from ever reaching the AgentRuntime registry.

## The Manifest Schema: openclaw.plugin.json and the Contracts Block

To prevent a plugin from being flagged as "non-capability" and to ensure its tools are correctly indexed, the openclaw.plugin.json file must move beyond simple identification. In the 2026.5.x SDK, the "non-capability" status is a diagnostic signal used by openclaw plugins inspect to denote a plugin that provides functional tools or routes but fails to register for any of the standardized "native" capabilities, such as model inference, speech processing, or image generation.

The technical solution lies in the contracts block of the manifest. By explicitly declaring tool ownership within this static metadata, the plugin satisfies the registry's need for "control-plane discovery" without requiring the gateway to execute the full runtime module during the startup phase. This is particularly relevant for dynamic tools like load_skill, which may have heavy dependencies that would otherwise stall gateway initialization.

### Required Fields in the 2026.5.x Manifest Schema

A robust manifest for a skill-management plugin requires several core sections to ensure it is not treated as a "legacy hook-only" or "non-capability" artifact:

| Section | Required Field | Type | Function |
| :--- | :--- | :--- | :--- |
| Root | id | string | Canonical ID for plugins.entries.<id> lookup |
| Root | configSchema | object | Inline JSON Schema for Zod-based validation |
| Contracts | tools | string[] | List of tool names (e.g., ["load_skill", "execute_skill"]) |
| Activation | startup | boolean | Determines if the plugin loads at gateway boot |
| Capabilities | kind | string | Categorizes the plugin (e.g., "context-engine") |

The inclusion of the contracts.tools array is the primary mechanism for elevating a plugin's status in the registry. When the gateway performs a "descriptor-only" setup, it reads these tool names and injects them into the agent's potential capability list. If the contracts block is missing, the registry identifies the plugin as "non-capability," which may lead the AgentRuntime to prioritize "native" provider tools during high-concurrency turns where context token management is at its limit.

## Dynamic Tool Registration via the Plugin SDK

While the manifest provides the static declaration, the actual registration of logic occurs within the plugin's entry point, typically an index.ts file that exports a register(api) function. The OpenClawPluginApi object injected by the core serves as a permission token; it is the only authorized interface for modifying the internal registry state.

To register load_skill and execute_skill for correct indexing, the developer must use the api.registerTool method. The 2026.5.x SDK requires a detailed TypeBox schema for the parameters object. If the parameters are missing or malformed, the AgentRuntime will skip the tool and report a diagnostic error in the gateway logs.

```typescript
import { Type } from "@sinclair/typebox";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

export default function register(api: OpenClawPluginApi) {
  api.registerTool({
    name: "load_skill",
    description: "Dynamically loads an AgentSkill into the current session.",
    parameters: Type.Object({
      skillSlug: Type.String({ description: "The slug from ClawHub or a local path." }),
      force: Type.Optional(Type.Boolean({ default: false }))
    }),
    async execute(_id, params) {
      // Integration logic with AgentSkills framework
      return { content: "" };
    },
  });

  api.registerTool({
    name: "execute_skill",
    description: "Executes a previously loaded skill with specific arguments.",
    parameters: Type.Object({
      skillName: Type.String(),
      args: Type.Record(Type.String(), Type.Any())
    }),
    async execute(_id, params) {
      // Execution logic for skill dispatch
      return { content: "" };
    },
  });
}
```

The AgentRuntime differentiates between required tools and optional tools. By default, tools registered via api.registerTool are available if the plugin is enabled. However, if a tool has significant side effects—as is common with execute_skill which might invoke shell commands—it is recommended to register it as { optional: true }. This forces an additional layer of user consent via the configuration file, ensuring that high-risk tools are not exposed to the agent without explicit administrative approval.

## Visibility and the Multi-Layered Permission Architecture

A common failure in the 2026.5.x environment occurs when a plugin is successfully loaded and indexed (visible via openclaw plugins inspect) but its tools remain invisible to the agent during chat sessions. This is a deliberate result of the framework's "multicast" tool-loading strategy, which seeks to minimize context token consumption by only providing the agent with the tools it actually needs for the current task.

The token cost for including a tool's full JSON schema in the system prompt can be substantial. For a tool with complex nested parameters, the overhead typically follows the formula:
$$T_{tool} \approx \sum_{i=1}^{n} (L_{name} + L_{desc} + L_{schema}) / 4$$
where $L$ represents the character length of the metadata. For a suite of skill-management tools, this can consume 500-1000 tokens per turn. To mitigate this, OpenClaw 2026.5.x enforces a three-gate visibility system:

1.  **The Loader Gate (plugins.allow):** This controls whether the plugin's code is even allowed to exist in the gateway's memory. If a plugin is not in the plugins.allow list, or if it is explicitly blocked by plugins.deny, it will not be registered.
2.  **The Registry Gate (tools.profile):** The global tool baseline, often set to "coding" or "full," determines if high-risk functional tools are eligible for use. Profiles like "minimal" or "messaging" will strip functional tools from the AgentRuntime even if the plugin is loaded.
3.  **The visibility Gate (tools.alsoAllow):** This is the specific configuration key required for external plugin tools. Even if a plugin is in plugins.allow, its tools are often withheld from the LLM unless the tool names are explicitly listed in tools.alsoAllow or agents.list.tools.allow.

| Configuration Key | Requirement | Impact on load_skill Visibility |
| :--- | :--- | :--- |
| plugins.allow | Mandatory | Enables plugin code to load and register tools |
| tools.profile | Mandatory | Must be set to "coding" or "full" for execution tools |
| tools.alsoAllow | Recommended | Explicitly permits the agent to "see" the plugin's tools |
| agents.list.tools.allow | Context-Specific | Restricts visibility to a specific agent persona |

The plugins.allow list is particularly sensitive. On every gateway restart, the loader resolves the allowlist; if the list is "open" or improperly configured, the gateway logs a series of warnings (warnWhenAllowlistIsOpen()) but proceeds to load via plugins.load.paths. However, this "loose" loading often leads to the "non-capability" flagging because the gateway lacks the metadata to correctly categorize the tools without an explicit allowlist entry or manifest contract.

## Solving the "Non-Capability" Registry Classification

To ensure a plugin is identified as a "Capability" rather than a "Non-Capability," it must participate in the standardized orchestration layer. The 2026.5.x architecture defines "capabilities" as the native plugin model that vendor plugins implement to provide typed contracts.

If the plugin’s only goal is to provide load_skill and execute_skill, it remains fundamentally functional. To bridge this gap and achieve a hybrid-capability or plain-capability signal in diagnostics, the plugin can be registered as a context-engine or memory extension. This is done via the kind field in the manifest:

```json
{
  "id": "skill-dynamic-engine",
  "kind": "context-engine",
  "contracts": {
    "tools": ["load_skill", "execute_skill"]
  },
  "configSchema": { "type": "object", "properties": {} }
}
```

When a plugin declares itself as a kind: "context-engine", the AgentRuntime assigns it to an "exclusive slot". Only one plugin can fill the contextEngine slot at a time, but this assignment ensures the plugin is treated as a core architectural component rather than an auxiliary functional tool. This status upgrade ensures the plugin is prioritized during the "tool descriptor planning" phase of the agent turn, reducing the latency associated with dynamic tool resolution.

## Technical Integration with the AgentSkills Framework

The dynamic tools load_skill and execute_skill essentially serve as a bridge to the AgentSkills system. An OpenClaw skill is not a plugin; it is a directory containing a SKILL.md file with instructions that tell the agent what to run and how to format the output. For these tools to be correctly indexed, they must understand the precedence of skill loading.

OpenClaw 2026.5.x uses a hierarchical precedence for skill matching:
1. Workspace Skills: <workspace>/skills/ (Highest) 
2. Project Agent Skills: <workspace>/.agents/skills/ 
3. Personal Agent Skills: ~/.agents/skills/ 
4. Managed Skills: ~/.openclaw/skills/ 
5. Bundled Skills: Standard library skills (Lowest) 

A dynamic tool like load_skill must be programmed to search these directories in order. Furthermore, the SKILL.md frontmatter may contain requires metadata, specifying necessary binaries (e.g., requires.bins: ["df", "ps"]). If the tool attempts to execute a skill whose requirements are not met on the host system, the AgentRuntime will block the execution, even if the tool itself is correctly indexed and visible.

| Skill Metadata Field | Type | Impact on Execution |
| :--- | :--- | :--- |
| command-dispatch | string | If set to "tool", bypasses LLM and runs a tool directly |
| command-tool | string | The specific tool to run when dispatched (e.g., "exec") |
| requires.bins | string[] | List of shell binaries required on the PATH |
| metadata.openclaw | object | JSON object for gating and platform restrictions |

For execute_skill to be robust, it should ideally respect the command-dispatch: tool pattern. This allows the agent to treat the skill as a deterministic command, which is essential for workflows like "wrapping a safe script with arguments" or "running a read-only report generator". By registering these tools within a plugin that declare its contracts, the developer creates a stable, manifest-validated bridge between the LLM and the filesystem.

## Security Hardening and TaskFlow Integration

The 2026.5.x release has significantly tightened the perimeter around tool execution. This is particularly relevant for dynamic tools, which are often the targets of path traversal or environment variable injection attacks. Any tool that interacts with the filesystem, such as load_skill, is subject to "fast path POSIX containment checks". These checks ensure that the resolved realpath of any skill or file stays within the configured workspace root; any attempt to access files outside this boundary results in an immediate EACCES or ENOENT error.

Furthermore, for long-running operations triggered by execute_skill, the plugin should utilize the api.runtime.taskFlow interface. This allows the plugin to create "Managed Task Flows," where the state is entirely persisted by OpenClaw. This decoupling is vital because it allows the agent to maintain its state even if the gateway restarts or the session is temporarily interrupted.

| Task Flow Sync Mode | Persistence Owner | Best Use Case |
| :--- | :--- | :--- |
| Managed | OpenClaw Core | Native skills and internal plugin tools |
| Mirrored | External Orchestrator | Integration with external systems like Chorus or Jira |

If a plugin tool fails to bind its tasks to a TaskFlow, it risks becoming an "orphaned session," which the gateway's task maintenance system will eventually close to reclaim resources. Correct indexing in the AgentRuntime therefore implies not just visibility, but also the ability for the tool to participate in the core task orchestration and lifecycle.

## Solving the "All Talk, No Action" Problem

Many developers find that their tools are indexed but the agent refuses to call them, responding instead with "all talk, no action." In the 2026.x series, this is usually caused by the tool policy layer. Even if load_skill is correctly registered, its effective tool policy may be "minimal" if the provider or model has not been granted sufficient permissions.

The policy resolution order is as follows:
1. Global tools.profile 
2. tools.byProvider[provider].profile 
3. Global tools.allow 
4. tools.byProvider[provider].allow 
5. agents.list.tools.allow 
6. Sandbox tool policy (if active) 

To resolve this, developers should use the openclaw sandbox explain --session <key> command. This will reveal the "mode" of the session (e.g., non-main or sandboxed) and any explicit tool denies. If the session is sandboxed, the tools load_skill and execute_skill must be added to the tools.sandbox.tools.allow list in the openclaw.json config.

## Troubleshooting and Diagnostics for the 2026.5.x Runtime

The openclaw doctor utility remains the most effective way to repair a fragmented registry. For plugins, the --fix flag can clean up stale aliases and quarantine invalid configurations that prevent tool indexing. When debugging dynamic tool registration, the following sequence is recommended for professional operators:

1.  **Status Check:** Run openclaw status --deep --require-rpc to confirm the active configuration path and gateway health.
2.  **Plugin Inspection:** Run openclaw plugins inspect <id> --runtime --json to verify that the SDK-level registration for load_skill and execute_skill was successful.
3.  **Config Validation:** Use openclaw config schema to ensure the openclaw.plugin.json matches the requirements for the installed version of the gateway.
4.  **Trace Logging:** Enable logging.level trace and look for "tool factory timing" to ensure the AgentRuntime is not stalling during prompt preparation.
5.  **Audit Fix:** Run openclaw security audit --fix to ensure that execution permissions are not being blocked by a global guardrail.

For plugins using the OpenClaw App SDK (the @openclaw/sdk package used for external integrations), developers must remember that the registration mechanics differ from the Plugin SDK. The App SDK communicates via RPC, whereas the Plugin SDK runs in-process. Only the Plugin SDK can register tools into the native AgentRuntime registry; external integrations must rely on the "loopback MCP bridge" or the "MCP adapter plugin" to expose tools to the agent.

## The Role of ClawHub in Tool Visibility

As of 2026.5, ClawHub has become the primary authority for plugin metadata. When a plugin is installed from ClawHub, the gateway records artifact metadata that simplifies the indexing process. For developers of dynamic tools, publishing to ClawHub provides a "verification" signal that can reduce the likelihood of tools being flagged as unsafe or "non-capability" by the built-in scanners.

However, ClawHub does not replace the need for a local openclaw.plugin.json. The manifest remains the "soul" of the plugin inside the gateway, defining how it presents its capabilities to the AgentRuntime. If a skill isn't on ClawHub, it can still be installed from npm, but developers must ensure the package.json includes the openclaw.extensions declaration to point the loader to the correct entry point.

## Summary of Best Practices for Dynamic Tool Registration

| Action | Context | Goal |
| :--- | :--- | :--- |
| Use contracts.tools | Manifest | Ensures static indexing and prevents "non-capability" flag |
| Set kind: "context-engine" | Manifest | Upgrades plugin to a native architectural capability |
| Use TypeBox schemas | SDK Code | Satisfies the AgentRuntime requirement for typed tool parameters |
| Add to tools.alsoAllow | Configuration | Makes tools visible to the agent's LLM system prompt |
| Implement TaskFlow | SDK Code | Persists tool state and manages long-running background work |
| Run openclaw doctor | CLI | Repairs the registry and cleans up stale plugin references |

In the high-density token environment of modern agents, the ability of a plugin to accurately and leanly declare its tools is not just a technical requirement but a performance necessity. By mastering the 2026.5.x manifest schema and the AgentRuntime registration methods, developers can build robust, dynamic systems that extend the capabilities of the OpenClaw assistant without compromising the security or stability of the host gateway.
