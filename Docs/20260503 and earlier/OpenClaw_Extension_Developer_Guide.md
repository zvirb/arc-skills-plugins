# OpenClaw Extension Developer Guide

## Overview

This guide provides the official, step-by-step methodology for developing native OpenClaw extensions (Skills and Plugins) in alignment with the **Lean Manufacturing Principles** (Kaizen, Standardized Work, Jidoka) and the **Architecture Pivot**.

In OpenClaw, capabilities are strictly divided into two layers:
1. **Plugins (The Runtime Layer):** TypeScript-based modules that execute code, manage state, and expose native tools.
2. **Skills (The Cognitive Layer):** Markdown-based instructions that teach the agent when and how to use tools.

---

## Part 1: Developing a TypeScript Plugin

Plugins are the only acceptable location for executable code. Never use Python scripts for OpenClaw orchestration.

### 1. Project Structure
A standard OpenClaw plugin must reside in the `Plugins/` directory and contain the following structure:
```text
Plugins/MyCustomPlugin/
├── src/
│   └── index.ts          # Main entry point exporting the register function
├── package.json          # Node dependencies and OpenClaw metadata
├── tsconfig.json         # TypeScript configuration
└── openclaw.plugin.json  # Plugin manifest
```

### 2. The Manifest (`openclaw.plugin.json`)
Every plugin must declare its metadata, permissions, and dependencies explicitly:
```json
{
  "id": "my-custom-plugin",
  "name": "My Custom Plugin",
  "version": "1.0.0",
  "description": "Exposes native API interactions.",
  "dependencies": []
}
```

### 3. The Implementation (`src/index.ts`)
Plugins must adhere to the `IPlugin` interface and use the `@openclaw/plugin-sdk`. You must export a `register` function.

**Critical Principles Applied:**
- **Jidoka (Self-Healing):** Always wrap execution in a `try/catch` and return strict JSON errors so the agent can auto-correct.
- **Config Validation:** Always validate inputs against a strict schema.

```typescript
import { PluginApi } from '@openclaw/plugin-sdk';
import { z } from 'zod';

// Define strict schemas for your tool arguments
const MyToolSchema = z.object({
  targetId: z.string().describe("The ID of the target resource."),
  action: z.enum(["start", "stop"]).describe("The action to perform.")
});

export async function register(api: PluginApi) {
  api.registerTool({
    name: 'my_custom_tool',
    description: 'Executes a specific action on a target resource.',
    schema: MyToolSchema,
    execute: async (args) => {
      try {
        // Validation & Execution Logic (Standardized Work)
        const validatedArgs = MyToolSchema.parse(args);
        
        // ... perform native Node.js operations ...
        const result = { status: "success", data: "Action completed." };
        
        // Truncate output to avoid Context Bloat
        return JSON.stringify(result);

      } catch (error) {
        // Jidoka: Deterministic Exit. Return actionable feedback.
        return JSON.stringify({
          success: false,
          error: `Execution failed. Please correct and retry. Details: ${error.message}`
        });
      }
    }
  });
}
```

### 4. Compilation & Deployment
Plugins must be compiled to JavaScript before installation:
```bash
npm run build
openclaw plugins install /path/to/plugin
openclaw gateway restart
```

---

## Part 2: Developing a Markdown Skill

Skills contain zero executable code. They are strict, concise operating procedures that configure the LLM's system prompt.

### 1. Structure (`SKILL.md`)
A skill must be placed in a dedicated folder inside `Skills/` and contain a `SKILL.md` file with YAML frontmatter.

### 2. The YAML Frontmatter
The frontmatter defines the skill's metadata and dependencies.
```yaml
---
name: My Custom Agent Skill
slug: my-custom-skill
version: 1.0.0
description: Teaches the agent to manage specific resources using native tools.
requires:
  plugins:
    - my-custom-plugin
  bins: []
---
```

### 3. The Markdown Body (Kaizen Prompts)
The body must be brutally concise. Avoid conversational language. Use strict algorithmic formatting.

```markdown
# Objective
Manage specific resources using the `my_custom_tool` tool.

# Standard Operating Procedure
1. WHEN the user requests an action on a resource, THEN parse the resource ID and requested action.
2. EXECUTE `my_custom_tool` with the following schema:
   ```json
   {
     "targetId": "<extracted-id>",
     "action": "<start|stop>"
   }
   ```
3. IF the tool returns an error, analyze the `error` field and retry up to 3 times (Jidoka).
4. Do NOT hallucinate commands or bypass the tool.
```

### 4. Agent Binding
Installing a skill is not enough. You must bind it to the agent profile:
1. Run `openclaw skills install /path/to/skill`
2. Open `~/.openclaw/openclaw.json`
3. Add `my-custom-skill` to `agents.list[0].skills`.
4. Restart your session.

---

## Part 3: Mandatory Validation Protocol

Before marking any extension as complete, you must physically verify it:
1. **The TUI:** Watch the execution loop via `openclaw tui` (press `[L]` for logs).
2. **Independent Verification:** Do not trust the tool's return code. If you modify a database or a Google Workspace app, use the `browser` tool or external queries to visually confirm the mutation.
