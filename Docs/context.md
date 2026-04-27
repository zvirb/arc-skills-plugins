# Documentation Context

This folder is the central location for all overarching Open Claw documentation, guides, and architectural notes.

## Guidelines

1. **Global Scope Only:** Only place documentation here that applies to the entire project or multiple components.
2. **Localize Specific Docs:** If documentation is specific to a single Skill or Plugin, it should be placed in that Skill's or Plugin's own sub-folder instead of here.
3. **Keep it Tidy:** Organize documents into logical sub-folders if this directory begins to grow.

## Core Documents

This folder contains foundational architectural guidelines for the OpenClaw ecosystem:
- `Architecture_Pivot_Strategy.md`: The primary source of truth regarding the pivot to a lightweight, local OpenClaw runtime driven by atomic TypeScript Plugins and Markdown Skills.
- `OpenClaw_Best_Practices_and_Common_Issues.md`: The primary source of truth for avoiding known anti-patterns and ensuring correct runtime validation.
- `OpenClaw_Extension_Developer_Guide.md`: The step-by-step methodology for building native OpenClaw extensions (Skills and Plugins) in alignment with Lean Manufacturing Principles.

## Development Mandates
1. **Extensive Research:** Before implementing any new capability, you MUST research tool/API documentation online to ensure schema and command accuracy.
2. **Independent Verification:** All Google Workspace mutations MUST be verified independently via the `browser` tool.

## Network & Infrastructure Notes
- **Ollama Configuration:** Ollama for access from WSL is on port `11450`. Ollama on Alienware (SSH) is on port `11434`.
