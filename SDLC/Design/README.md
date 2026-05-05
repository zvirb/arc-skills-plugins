# SDLC Domain 2: Design

## Purpose
The Design domain focuses on the "Contract Principle"—defining the formal structures and interaction patterns that govern agent behavior. This phase ensures that probabilistic AI execution is constrained by deterministic interfaces.

## Documents
- **[2.1 Technical Specification](./2.1_Technical_Specification.md)**: RFC-style documentation of the system's architecture.
- **[2.2 Schema Definition](./2.2_Schema_Definition.md)**: Formalizing I/O contracts using JSON Schema or Pydantic.
- **[2.3 Prompt Design Patterns](./2.3_Prompt_Patterns.md)**: Implementing specialized reasoning structures (ReAct, SGR, Reflect).
- **[2.4 Tool & API Design](./2.4_Tool_Design.md)**: Designing deterministic interfaces for actuators.

## Workflows
- `design-spec`: Draft a technical specification for the project.
- `design-schema`: Generate validated JSON schemas for all nodes.
- `design-verify`: Schema-first verification of the system architecture.

## Jidoka Gate
The Design phase is considered complete only when the **Full System Schema** is locked and validated for cross-node compatibility. No "natural language" hand-offs are permitted between nodes.
