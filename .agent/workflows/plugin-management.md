---
name: Native Plugin Lifecycle Management
description: Scaffold complex Node.js/TypeScript modules for custom API routes, database bridges, or novel tool wrappers.
---

# Native Plugin Lifecycle Management

This workflow manages the lifecycle of OpenClaw Plugins to ensure robust state management and proper SDK utilization.

## Steps

1. **Scaffold Plugin Directory:** Create the designated sub-folder within the `Plugins/` directory.
2. **Initialize Environment:** Initialize the TypeScript/Node.js environment with a precise `package.json` manifest.
3. **Configure Manifest:** Generate the mandatory `openclaw` object, map the `extensions` array, and define strict `compat` versioning within `package.json`.
4. **Validation Gate (SDK Usage):** Statically verify that all imports utilize the focused subpath SDK convention (e.g., `openclaw/plugin-sdk/plugin-entry`) and that no monolithic root imports are used.
5. **Validation Gate (Hooks):** Verify that the `definePluginEntry` wrapper is used, the `register(api)` hook is properly instantiated, and the `configSchema` is fully validated.
6. **Final Check:** Request execution of `openclaw plugins list --verbose` to ensure the module survives the 8-step load pipeline.
