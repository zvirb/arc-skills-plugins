# SDLC Domain 1: Discovery

## Purpose
The Discovery domain is focused on transforming high-level human intent into concrete, actionable, and atomic requirements. This phase establishes the "Standardized Work" foundation necessary for autonomous execution.

## Documents
- **[1.1 Problem Framing](./1.1_Problem_Framing.md)**: Defining the specific purpose and PEAS (Performance, Environment, Actuators, Sensors) of the agent.
- **[1.2 Requirement Gathering](./1.2_Requirement_Gathering.md)**: Structured artifact creation and "Spec First" contracts.
- **[1.3 Decomposition Planning](./1.3_Decomposition_Planning.md)**: Breaking complex goals into specialized sub-agents and micro-nodes.
- **[1.4 Feasibility & Risk Analysis](./1.4_Feasibility_Analysis.md)**: Evaluating VRAM constraints, data quality, and governance requirements.

## Workflows
- `discovery-init`: Initialize a new project discovery session.
- `discovery-decompositon`: Automated goal decomposition into atomic nodes.
- `discovery-verify`: Independent verification of discovery artifacts.

## Jidoka Gate
The Discovery phase is considered complete only when the **Master Atomic Node List** is generated and validated against the system's VRAM/Compute constraints.
