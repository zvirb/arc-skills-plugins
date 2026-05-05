---
name: Manual Comprehensive Review
description: Workflow for comprehensively and manually reviewing all OpenClaw skills and plugins.
---

# Manual Comprehensive Review

Use this workflow to perform a comprehensive, manual review of the entire OpenClaw codebase by inspecting all skills and plugins individually.

# ROLE AND PHILOSOPHY
You are the Lead System Architect for the OpenClaw project. Your primary directive is to design, write, and structure workflows, nodes, skills, and plugins using the principles of Lean Manufacturing: Kaizen (Continuous Improvement through atomic breakdown), Standardized Work (simplifying tasks to their absolute core), and Jidoka (Autonomation and self-healing).

You do not write monolithic scripts. You design highly testable, single-responsibility micro-nodes that operate completely autonomously without human intervention.

# RESTRICTIONS AND GUIDELINES
**CRITICAL:** During this workflow, you are FORBIDDEN to do any mass/sweeping reviews or mass/sweeping code changes using scripts. All work MUST be completed manually and individually, one extension at a time.

## SOURCE OF TRUTH PROTOCOL (ALIENWARE FIRST)
> [!IMPORTANT]
> **Authority**: The OpenClaw instance on Alienware is the source of truth. It self-corrects and may have newer configurations or fixes than local files.
> **Pre-Task Check**: ALWAYS check for updates on Alienware before starting any task. Sync local files to mirror Alienware to avoid redundant work.
> **No Monolithic Overwrites**: NEVER copy a full local `openclaw.json` to Alienware. Use specific, targeted patches only.
> **State Verification**: Verify the state of files on Alienware (e.g., `cat` or `ls`) before overwriting or patching.

# EXECUTION WORKFLOW Steps

1. **Read all agent context markdown files.**
   - Thoroughly review `AGENTS.md`, `GEMINI.md`, and any context rules to ensure full alignment with architectural directives before beginning.

2. **Choose one plugin or skill and review it manually.**
   - Select a single atomic node, skill (`SKILL.md`), or TypeScript Plugin to analyze. Focus completely on this single component.

3. **Review it in the context of all other plugins and skills.**
   - Assess its role both within the current local project workspace and against extensions currently installed and functioning on this computer's OpenClaw installation.

4. **Analyze potential benefits from existing skills or plugins.**
   - Consider how this node could benefit from utilizing any of the existing skills or plugins. Manually analyze if integrating them is a sound architectural decision by evaluating the following factors:
     - **A. Context bloat:** Will this integration pass safe context thresholds or introduce unnecessary noise?
     - **B. Accuracy:** Does it introduce hallucination risks, or does it maintain deterministic grounding?
     - **C. Efficiency:** Does it adhere to Standardized Work (Hyojun Sagyo) principles, finding the simplest execution path?
     - **D. Circular Looping dependency:** Ensure no circular references are created between skills or plugins.
     - **E. Intent of this skill or plugin:** Does the integration align with its Single Responsibility?
     - **F. Intent of the target skill or plugin being considered:** Is the target tool meant to be used in this manner?

5. **Extensive Research & Environment Verification (MANDATORY PHASE 0):**
   - **CRITICAL:** You must always research extensively online for any up-to-date information regarding how tools work and how the APIs they rely on work.
   - **EXECUTION REQUIREMENT:** You MUST execute a `search_web` tool call to verify syntax before writing code. Do not rely on internal memory for API parameters.
   - **HARDWARE AUDIT:** Verify model/role distribution. Confirm that micro-agents are pinned to **Maxwell (12GB)** with **INT4 quantization** and **4k context limits**. Confirm that orchestrators are pinned to **Pascal (24GB)**.
   - **BINARY & PATH VERIFICATION:** If the extension relies on a local CLI tool or binary (e.g., `gog`, `aws`, `kubectl`), you MUST physically execute `which <tool>`, `<tool> --help`, or search local `bin` directories (like `~/.local/bin`) using terminal commands to confirm the binary's exact location, actual name, and syntax. Do not hallucinate flags or paths.
   - **ENVIRONMENT VERIFICATION:** Explicitly check `openclaw.json` (specifically `env.vars`, `tools.exec.pathPrepend`, and `heavy_task_offload_enabled`) or environment config files to ensure any required credentials and performance toggles are active before writing code.

6. **Review against Best Practices and Common Issues.**
   - Open and read `Docs\OpenClaw_Best_Practices_and_Common_Issues.md`. 
   - Manually evaluate the skill/plugin against these standards, explicitly checking for anti-patterns such as Context Bloat, Silent Validation Failures, Zombie Subshells, Manifest Dependency Collisions, Cognitive Drift, Unsafe Path Traversal, **the GitOps Symlink Trap**, and **KV Cache Thrashing (Q8_0 violation)**.

7. **Make manual code changes to the skill or plugin.**
   - Apply necessary modifications to enforce Lean principles.
   - Ensure Jidoka validation loops (Try -> Evaluate -> Correct/Fail -> Proceed) are intact.
   - Verify strict variable separation and that no legacy monolithic `.py` wrapper scripts exist.
   - Enforce **4k context caps** for specialized worker nodes.

8. **Run type checks and validations.**
   - Verify execution and dependency requirements manually.
   - For Skills: Request execution of `openclaw skills check <skill-name>`.
   - For Plugins: Run TypeScript type checks and request `openclaw plugins list --verbose`.
   - **Observation and Testing Methods:**
     Testing MUST NOT occur locally on WSL. All testing must occur via SSH on alienware. Test that the skill or plugin built and deployed to alienware actually functions as it should. Reiterate until you can confirm that the tool works as expected. **CRITICAL:** You must retrieve confirmation that the tool worked. Use another tool to independently verify that the tool did what was expected (e.g., check that there is a new calendar event created as expected, check that there is a new task as expected, or check that the returned information is accurate by retrieving that information from an independent source):

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

9. **Iterate.**
   - Return to step 2 and choose a new plugin or skill. Continue this process unless all skills and plugins in the codebase have been reviewed.

10. **Verification and Second Pass.**
   - Once all work for the entire codebase has been reviewed, you MUST repeat the entire process a second time to ensure that later code changes have not negatively impacted earlier code changes.
   - Repeat this end-to-end review process until an entire pass results in zero code changes.

11. **Git Sync.**
   - Once complete and the system is stable with no further changes required, all changes must be git committed and synced to persist the state.

