# Documentation Context

This folder is the central location for all overarching Open Claw documentation, guides, and architectural notes.

## Guidelines

1. **Global Scope Only:** Only place documentation here that applies to the entire project or multiple components.
2. **Localize Specific Docs:** If documentation is specific to a single Skill or Plugin, it should be placed in that Skill's or Plugin's own sub-folder instead of here.
3. **Keep it Tidy:** Organize documents into logical sub-folders if this directory begins to grow.

## Research Documents

This folder contains foundational research and architectural guidelines for the OpenClaw ecosystem:
- `AI Assistant Skills & Architecture Analysis.docx`: Architectural specification detailing neuro-symbolic integration, isolated micro-VMs, and evaluation-optimizer loops.
- `OpenClaw Skills Research for Productivity.docx`: Gap analysis detailing custom builds for OpenClaw, including integration with OpenProse, CatchMe, LanceDB, and Lobster.
- `OpenClaw Extension Developer Guide.docx`: Guidelines for building extensions and plugins.

**⚠️ CRITICAL WARNING REGARDING RESEARCH DOCS:** 
Some of these legacy research documents reference Kubernetes or Docker infrastructure. **IGNORE** all such references. The project direction has pivoted: we are replacing the entire stack with pure OpenClaw skills, plugins, and lightweight open-source applications. Do not attempt to scaffold K8s manifests or Dockerfiles based on these documents.
