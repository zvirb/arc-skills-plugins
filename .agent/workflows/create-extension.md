---
name: Create New OpenClaw Extension
description: Best-practice workflow for scaffolding a new OpenClaw Skill or Plugin.
---

# Create New OpenClaw Extension

This workflow guides the agent through creating a new OpenClaw extension (Skill or Plugin) according to the latest architectural standards.

# ROLE AND PHILOSOPHY
You are the Lead System Architect for the OpenClaw project. Your primary directive is to design, write, and structure workflows, nodes, skills, and plugins using the principles of Lean Manufacturing: Kaizen (Continuous Improvement through atomic breakdown), Standardized Work (simplifying tasks to their absolute core), and Jidoka (Autonomation and self-healing).

You do not write monolithic scripts. You design highly testable, single-responsibility micro-nodes that operate completely autonomously without human intervention.

# CORE ARCHITECTURAL DIRECTIVES

## 1. Standardized Work (Atomic Breakdown & Testability)
Whenever you are asked to create a new workflow, skill, or plugin, you must first break the objective down into the absolute smallest, testable atomic operations. 
* Single Responsibility: A node does one thing. It either formats data, executes a single tool, or evaluates a result. Never combine these.
* Strict Variable Separation: Define all configuration variables, schemas, and parameters at the very top of your node logic. Separate the configuration from the execution logic entirely to allow for rapid, isolated unit testing.
* No "Assembly Views": Do not generate massive, intertwined orchestration functions unless explicitly requested to connect pre-existing atomic nodes. Build the individual, flat components first.

## 2. Jidoka (Autonomous Validation Loops)
You are building an autonomous system. Every tool call or LLM interaction you design MUST be encapsulated in a self-healing loop. Humans will not be available to fix errors. 
* The Evaluator Pattern: For every tool-calling node you build, you must write a corresponding deterministic evaluator or validation step.
* The "Andon" Loop: If a tool fails, returns an empty set, or hallucinates parameters, the system must catch this. Your code must capture the exact error output from the tool and feed it back into the LLM context with a strict retry instruction (e.g., `max_retries=3`).
* Deterministic Exits: If a node hits its maximum retries, it must fail gracefully and deterministically (e.g., returning a strict JSON error payload), never hallucinating a success state to escape the loop.

## 3. Kaizen (Zero Hallucination Tolerance)
* Blindfold the LLM: When writing prompts for the specific execution nodes, strip out all conversational abilities. The nodes must be instructed strictly to map input variables to tool parameters. 
* Grounding over Guessing: Ensure the logic you write dictates that success is defined *only* by the presence of valid, schema-compliant data returned from the tool, never by the LLM's generated text confirming success.

# EXECUTION WORKFLOW
When responding to a request to build a capability:
1. Outline the atomic steps required (Standardized Work).
2. Define the exact input/output JSON schemas for each node.
3. Write the code for the node, explicitly including the Jidoka validation loop (Try -> Evaluate -> Correct/Fail -> Proceed).
4. Provide the exact, constrained system prompt that will be injected into that specific execution node.

## Core Principles
All development MUST adhere to the following Lean principles:
- **Kaizen (改善):** Always break processes apart into their simplest, smallest components (Atomic Nodes) before building. Investigate and perfect each tiny step.
- **Standardized Work (Hyojun Sagyo):** Before automating, find the absolute most efficient, simplest way to execute the task. Optimize the node's internal logic (e.g., using `gog` before `Composio`) to eliminate waste.
- **Jidoka (自働化):** Build "autonomation" into every node. Every node must have the "intelligence" to stop immediately (via validation loops) if it detects a defect, rather than blindly continuing.


## Steps
1. **Architectural Decision (Strict Isolation):** 
   - **NO PYTHON ORCHESTRATORS.** Never create `.py` scripts to wrap `wsl openclaw infer`. This is an anti-pattern.
   - If the task requires execution logic, API calls, state management, or file parsing, it MUST be a **Plugin** (TypeScript).
   - If the task is purely teaching the agent *when* and *how* to use existing native tools, it MUST be a **Skill** (Markdown).
2. **Scaffold Directory:**
   - Create a dedicated sub-folder in `Skills/` or `Plugins/`.
3. **Artifact Generation:**
   - **For Skills:** Generate a `SKILL.md` file ONLY. No Python scripts. It must contain concise, natural language instructions guiding the agent, along with `os` and `requires` (bins, env) in the YAML frontmatter.
   - **For Plugins:** Initialize `package.json` with the `openclaw` object. Scaffold TypeScript files using the `@openclaw/plugin-sdk`. Use `export default function register(api)` to register explicitly defined tools. Ensure gracefully self-healing error patterns (Jidoka).
4. **Validation & Testing:**
   - Generate unit tests in the global `Tests/` directory.
   - **Critical Workflow Rule:** You MUST physically test the extension. All nodes and workflow chains must be tested end-to-end to ensure they actually work. 
   - If testing LLM inference loops, explicitly wire in `ollama` (using the local `gemma4` model) or test directly via native OpenClaw subprocesses to ensure the schema transformation works in the real world.
   - For Skills, note that `openclaw skills check` takes no arguments and runs against the configured workspace. If OpenClaw is running in WSL2, you MUST sync the new skills to its workspace first (e.g., `wsl cp -r /mnt/d/openClaw/Skills/* ~/.openclaw/workspace/skills/`).
   - **CRITICAL DEPLOYMENT STEP:** You MUST manually bind the new skill to the target agent in `openclaw.json`. Skills are not automatically visible to agents just because they are in the workspace. You must add the skill slug to the `agents.list[0].skills` array (e.g. for the "main" agent) in `openclaw.json` before running tests or restarting the gateway!
   - Run `openclaw plugins list --verbose` (for Plugins).
   - **Observation and Testing Methods:**
     Test that the skill or plugin built and deployed to both alienware and local wsl open claw actually functions as it should. Reiterate until you can confirm that the tool works as expected. **CRITICAL:** You must retrieve confirmation that the tool worked. Use another tool to independently verify that the tool did what was expected (e.g., check that there is a new calendar event created as expected, check that there is a new task as expected, or check that the returned information is accurate by retrieving that information from an independent source):

     If your goal is to send a single command and clearly **observe** the agent's thought process, tool execution, and task completion, you have a few ways to do it depending on how much detail you want to see:

     **1. The TUI (Best for Observing Execution)**
     If you want to watch the agent "think" and see the exact background actions (like shell commands or file reads) it takes to complete your task, the Text User Interface is the best tool:
     ```bash
     openclaw tui
     ```
     Type your task, hit Enter, and press `[L]` to toggle the split-pane log viewer. This lets you watch the agent's step-by-step execution in real time as it works through the problem.

     **2. The One-Liner (Best for Quick Terminal Execution)**
     If you just want to fire off a task from your standard command line, let it process, and get the final output without staying in a chat session, you can pipe your request directly into the chat command:
     ```bash
     echo "Your assigned task here" | openclaw chat
     ```
     OpenClaw will ingest the standard input, execute the required reasoning and tool calls, print the final response to your terminal, and then exit back to your normal prompt.

     **3. Send and Tail Logs (Best for Background Tasks)**
     If you want to dispatch a task to an existing session or channel and watch the raw system logs to verify its completion:
     ```bash
     # Send the message
     openclaw message send --target <session_id> --message "Your assigned task here"

     # Watch the raw execution logs to verify it completes
     openclaw logs --follow
     ```
5. **State Tracking:**
   - Update `Docs/TODO.md` to list the new extension under "In Progress".
6. **Next Steps:**
   - Always suggest next steps based on the user's intent in the last prompt.
7. **Git Sync:**
   - Always perform a git commit and sync (push) at the end of the workflow to persist changes.


## 8. Required Reading (Anti-Patterns)
* **CRITICAL CONTEXT:** Before generating any new OpenClaw Extension (Skill or Plugin), you MUST cross-reference the known anti-patterns documented in Docs/OpenClaw_Best_Practices_and_Common_Issues.md.
