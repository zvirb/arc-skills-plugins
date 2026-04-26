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

## Execution Workflow Steps

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

5. **Review against Best Practices and Common Issues.**
   - Open and read `Docs\OpenClaw_Best_Practices_and_Common_Issues.md`. 
   - Manually evaluate the skill/plugin against these standards, explicitly checking for anti-patterns such as Context Bloat, Silent Validation Failures, Zombie Subshells, Manifest Dependency Collisions, Cognitive Drift, and Unsafe Path Traversal.

6. **Make manual code changes to the skill or plugin.**
   - Apply necessary modifications to enforce Lean principles.
   - Ensure Jidoka validation loops (Try -> Evaluate -> Correct/Fail -> Proceed) are intact.
   - Verify strict variable separation and that no legacy monolithic `.py` wrapper scripts exist.

7. **Run type checks and validations.**
   - Verify execution and dependency requirements manually.
   - For Skills: Request execution of `openclaw skills check <skill-name>`.
   - For Plugins: Run TypeScript type checks and request `openclaw plugins list --verbose`.

8. **Iterate.**
   - Return to step 2 and choose a new plugin or skill. Continue this process unless all skills and plugins in the codebase have been reviewed.

9. **Verification and Second Pass.**
   - Once all work for the entire codebase has been reviewed, you MUST repeat the entire process a second time to ensure that later code changes have not negatively impacted earlier code changes.
   - Repeat this end-to-end review process until an entire pass results in zero code changes.

10. **Git Sync.**
   - Once complete and the system is stable with no further changes required, all changes must be git committed and synced to persist the state.
