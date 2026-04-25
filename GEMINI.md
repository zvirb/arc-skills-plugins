# Global Workspace Directives: OpenClaw Ecosystem

## 1. Architectural Distinction
* **CRITICAL:** Always evaluate the intent before writing code. If the goal requires complex application state or new endpoints, default to a Plugin. If it requires teaching the agent to orchestrate existing tools (e.g., `curl`, `jq`, `browser`), default to a Skill.

## 2. Testing and Validation Mandates
* Do not mark any code generation task as complete until local verification commands have been run.
* For Skills: You must request execution of `openclaw skills check <skill-name>` to verify syntax and dependency eligibility.
* For Plugins: You must request execution of `openclaw plugins list --verbose` to ensure the module survives the 8-step load pipeline.

## 3. Architectural Pivot (No Kubernetes/Docker)
* **CRITICAL ARCHITECTURE NOTE:** We are actively replacing the legacy Kubernetes/Docker stack with a lightweight architecture consisting solely of OpenClaw Skills and Plugins, supplemented by a few lightweight open-source applications.
* You must completely ignore any legacy research documentation, instructions, or workflows that mandate or mention Kubernetes, Docker, Flux CD, Kustomize, Pods, or CRDs.
* Focus entirely on native OpenClaw runtime execution and local environment dependencies.

## 4. Continuous Learning & Knowledge Preservation
* Whenever a lesson is learned, a bug is fixed, or a new pattern is established during attempted work, you MUST immediately update the relevant skills, agent context files (`context.md`, `AGENTS.md`), or workflow steps to encode this new knowledge. Do not rely on conversation memory.
