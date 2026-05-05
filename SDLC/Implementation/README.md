# SDLC Domain 3: Implementation

## Purpose
The Implementation domain focuses on "Standardized Work"—constructing atomic nodes and plugins that adhere strictly to the designs and schemas defined in earlier phases. This phase is where intent becomes executable logic.

## Documents
- **[3.1 Atomic Node Construction](./3.1_Atomic_Nodes.md)**: Building single-responsibility units of work.
- **[3.2 Prompt Engineering](./3.2_Prompt_Engineering.md)**: Implementing the reasoning patterns defined in the Design phase.
- **[3.3 TypeScript Plugin Development](./3.3_Plugin_Development.md)**: Building native OpenClaw plugins for complex logic.
- **[3.4 Skill Authoring (Markdown)](./3.4_Skill_Authoring.md)**: Teaching the agent how to use existing tools.

## Workflows
- `impl-node`: Scaffold a new atomic node or skill.
- `impl-plugin`: Initialize a new TypeScript plugin from the SDK.
- `impl-verify`: Local unit testing of implemented components.

## Jidoka Gate
The Implementation phase is considered complete only when every node passes its **Local Unit Test** and is verified against the **Blindfold Prompt** constraint. No monolithic scripts are allowed.
