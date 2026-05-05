# SDLC Domain 5: Delivery

## Purpose
The Delivery domain focuses on the secure, deterministic transition of validated components into the production environment. This phase ensures that agents are correctly bound to their capabilities and that deployments are traceable and reversible.

## Documents
- **[5.1 Automated Deployment Pipeline](./5.1_Deployment_Pipeline.md)**: Standardizing the push-to-production flow.
- **[5.2 Plugin Registry & Compilation](./5.2_Plugin_Registry.md)**: Managing the lifecycle of native extensions.
- **[5.3 Agent Binding & Capability Injection](./5.3_Agent_Binding.md)**: Configuring the agent roster and `openclaw.json`.
- **[5.4 Version Control & Rollback](./5.4_Version_Control.md)**: Ensuring every behavior change is versioned and reversible.

## Workflows
- `delivery-deploy`: Compile, install, and bind a new extension.
- `delivery-audit`: Verify the active configuration against the Git source of truth.
- `delivery-rollback`: Revert to a known stable version of a skill or plugin.

## Jidoka Gate
The Delivery phase is considered complete only when the **Active Configuration** in `openclaw.json` matches the **Git Source of Truth** and the agent successfully responds to a "Heartbeat" task using the new capability.
