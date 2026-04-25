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
1. **Architectural Decision (Kaizen):** 
   - Identify the user's goal and decompose it into the smallest possible atomic units.
   - If it involves orchestrating existing tools (e.g., curl, browser, Python scripts), default to a **Skill**.
   - If it requires complex application state, new API endpoints, database bridges, or native hooks, default to a **Plugin**.
2. **Scaffold Directory:**
   - Create a dedicated sub-folder in `Skills/` or `Plugins/`.
3. **Artifact Generation:**
   - **For Skills:** Generate a `SKILL.md` with concise, explicit instructions. Follow the "one skill, one responsibility" principle. Enforce security (never concatenate raw shell strings). Add `os` and `requires` (bins, env) to the YAML frontmatter.
   - **For Plugins:** Initialize `package.json` with the `openclaw` object and strict `compat` versioning. Scaffold TypeScript files using the official SDK (`openclaw/plugin-sdk/plugin-entry`) and `register(api)`. Ensure the plugin fails gracefully.
4. **Validation & Testing:**
   - Generate unit tests in the global `Tests/` directory.
   - **Critical Workflow Rule:** You MUST physically test the extension. All nodes and workflow chains must be tested end-to-end to ensure they actually work. 
   - If testing LLM inference loops, explicitly wire in `ollama` (using the local `gemma4` model) or test directly via native OpenClaw subprocesses to ensure the schema transformation works in the real world.
   - For Skills, note that `openclaw skills check` takes no arguments and runs against the configured workspace. If OpenClaw is running in WSL2, you MUST sync the new skills to its workspace first (e.g., `wsl cp -r /mnt/d/openClaw/Skills/* ~/.openclaw/workspace/skills/`) before running `wsl openclaw skills check` to verify syntax.
   - Run `openclaw plugins list --verbose` (for Plugins).
5. **State Tracking:**
   - Update `Docs/TODO.md` to list the new extension under "In Progress".
6. **Next Steps:**
   - Always suggest next steps based on the user's intent in the last prompt.
7. **Git Sync:**
   - Always perform a git commit and sync (push) at the end of the workflow to persist changes.
