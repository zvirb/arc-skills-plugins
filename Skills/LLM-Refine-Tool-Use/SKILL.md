---
name: LLM-Refine-Tool-Use
description: Teaches the agent to use the ToolStrategyEngine plugin to check for tool constraints before executing complex tools, and to record failures to prevent future hallucinations.
requires:
  bins: []
  env: []
os: ["windows", "linux", "darwin"]
---

# LLM Refine Tool Use

You are an expert Tool Strategy planner. Before you execute a task involving multiple tools, or when you are uncertain about the specific arguments required for a tool, you must consult the historical ledger to prevent hallucinations.

## Workflow Instructions

### 1. Planning Phase (Preventing Hallucination)
Whenever you are about to use a tool (especially native OS commands or complex plugins), you must first check if there are known constraints or anti-patterns for that tool.
- **Action:** Call the `get_tool_constraints` tool provided by the `ToolStrategyEngine` plugin.
- **Input:** Pass an array of the tool names you intend to use.
- **Result:** You will receive a list of `known_errors` and `argument_rules` for those tools. You MUST strictly adhere to these rules when formulating your final tool call.

### 2. Execution and Recording Phase (Jidoka)
If you execute a tool and it fails due to a schema mismatch, a missing argument, or a hallucinated parameter:
- **Action:** Stop immediately.
- **Action:** Call the `record_tool_failure` tool provided by the `ToolStrategyEngine` plugin.
- **Input:** 
  - `tool_name`: The name of the tool that failed.
  - `error_encountered`: The exact error message or a concise summary of the hallucination.
  - `argument_rule`: The corrected rule that must be followed in the future (e.g., "Must provide 'Cwd' parameter, do not use 'cwd'").

By consistently using these native tools, you will build a self-improving, hallucination-resistant memory for the entire OpenClaw ecosystem.
