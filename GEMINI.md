# Global Workspace Directives: OpenClaw Ecosystem

## 1. Architectural Distinction (Kaizen 改善)
* **CRITICAL:** Decompose all intent into the smallest possible atomic components before writing code. If the goal requires complex application state or new endpoints, default to a Plugin. If it requires teaching the agent to orchestrate existing tools (e.g., `curl`, `jq`, `browser`), default to a Skill.

## 2. Standardized Work (Hyojun Sagyo)
* Prerequisite to automation. Identify the absolute most efficient manual/CLI execution path for a task before wrapping it in a node.
* Do not mark any code generation task as complete until local verification commands have been run.
* For Skills: You must request execution of `openclaw skills check <skill-name>` to verify syntax and dependency eligibility.
* For Plugins: You must request execution of `openclaw plugins list --verbose` to ensure the module survives the 8-step load pipeline.

## 3. Jidoka (自働化)
* Implement "autonomation" by embedding self-healing loops and output validation into every node. 
* A node MUST stop immediately and report the error if it cannot achieve a valid state, rather than blindly continuing.

## 4. Architectural Pivot (No Kubernetes/Docker)
* **CRITICAL ARCHITECTURE NOTE:** We are actively replacing the legacy Kubernetes/Docker stack with a lightweight architecture consisting solely of OpenClaw Skills and Plugins, supplemented by a few lightweight open-source applications.
* **Google Workspace Exception:** The core ecosystem relies heavily on Google Workspace (Gmail, Calendar, Tasks, Drive, Docs, Sheets). You do NOT need to find or suggest open-source alternatives for these specific services; integrate directly with them.
* You must completely ignore any legacy research documentation, instructions, or workflows that mandate or mention Kubernetes, Docker, Flux CD, Kustomize, Pods, or CRDs.
* Focus entirely on native OpenClaw runtime execution and local environment dependencies.

## 4. Continuous Learning & Workflow Evolution
* Whenever a lesson is learned, a bug is fixed, or a new pattern is established during attempted work, you MUST immediately update the relevant skills, agent context files (`context.md`, `AGENTS.md`), or workflow steps to encode this new knowledge. 
* **Supplemental Tooling:** If you identify that a workflow requires supplemental tooling or missing steps to function correctly (e.g., viewing a DB, installing a missing local binary), you MUST add those explicitly to the workflow or skill documentation. Do not rely on conversation memory.
* **Online Research for Mocks:** Always perform online research to replace any mock functions. Ensure you are operating with the latest and best practices to supplement your knowledge when you lack specific implementation details.

## 5. Lean Manufacturing Principles
* **Kaizen (改善):** "Continuous improvement." Break processes apart (改) into simplest components and perfect (善) those tiny steps. Every node/skill must be an Atomic Node.
* **Standardized Work (Hyojun Sagyo):** Prerequisite to automation. Find the absolute most efficient, simplest manual way (SOP) before automating.
* **Jidoka (自働化):** "Autonomation" or "automation with a human touch." Automated processes must be intelligent enough to stop immediately upon detecting a defect (strict validation/error handling) to prevent cascading failures.
