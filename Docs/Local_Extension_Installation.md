# OpenClaw Local Extension Installation Guide

When developing OpenClaw skills and plugins locally (unmanaged extensions), a simple directory copy (`cp -r`) is often insufficient. OpenClaw relies on a strictly typed configuration manifest (`openclaw.json`) to register, enable, and securely load extensions.

Follow these best practices to ensure OpenClaw correctly recognizes and uses your locally developed extensions.

## Compiling Plugins for Use

OpenClaw plugins are typically written in native TypeScript (ESM) and must be compiled to JavaScript before the OpenClaw gateway can load them.

1. **Verify Manifests:** Ensure your plugin has a valid `package.json` with `type: "module"`, a `tsconfig.json` targeting a modern ECMAScript version (e.g., `ES2022`), and the mandatory `openclaw.plugin.json` manifest.
2. **Compile Source Code:** Run the build script to execute the TypeScript compiler (`tsc`), which translates your `src/` files into a `dist/` folder.
   ```bash
   cd /path/to/your/plugin
   npm install
   npm run build
   ```
3. **Check Entry Points:** Verify that the `openclaw.extensions` field in your `package.json` correctly points to the compiled `.js` files in the `dist/` directory, not the `.ts` source files.

## Installing Local Plugins

1. **Resolve Dependencies:** Ensure all Node.js dependencies are installed within your plugin's local directory before attempting installation.
   ```bash
   cd /path/to/your/plugin
   npm install
   ```
2. **Install via CLI:** Use the OpenClaw CLI to securely copy and register the plugin. Do not manually copy the folder to the plugins directory.
   ```bash
   openclaw plugins install /path/to/your/plugin
   ```
3. **Update Configuration:** If your plugin requires specific configuration (e.g., API keys, environment variables), you must manually edit the global configuration file.
   - Open `~/.openclaw/openclaw.json`
   - Locate the `plugins.entries` section.
   - Add or update the configuration for your plugin ID:
     ```json
     "plugins.entries": {
       "my-local-plugin": {
         "enabled": true,
         "config": {
           "API_KEY": "your-secret-key"
         }
       }
     }
     ```
4. **Restart the Gateway:** The OpenClaw Gateway must be restarted to resolve the new dependency graph.
   ```bash
   openclaw gateway restart
   ```
5. **Verify:**
   ```bash
   openclaw plugins list
   ```

## Installing Local Skills

Skills (which teach the agent cognitive directives via `SKILL.md`) have a hierarchical loading precedence. Workspace skills (`<workspace>/skills/`) take priority over global (`~/.openclaw/skills/`) and bundled skills.

1. **Install via CLI (Recommended):** The safest way to inject a local skill is via the CLI.
   ```bash
   openclaw skills install /path/to/local/skill
   ```
2. **Manual Copy (Alternative):** If you must script a manual sync (e.g., via `rsync` or `cp`), copy the directory to the global or workspace skills folder.
   ```bash
   cp -r /path/to/local/skill ~/.openclaw/workspace/skills/
   ```
3. **Update Configuration:** If manually copied, the skill is not automatically enabled or configured. You must update the engine's configuration.
   - Open `~/.openclaw/openclaw.json`
   - Locate the `skills.entries` section.
   - Register the skill to ensure it is explicitly enabled:
     ```json
     "skills.entries": {
       "my-local-skill": {
         "enabled": true,
         "env": {
           "CUSTOM_VAR": "value"
         }
       }
     }
     ```
     ```
4. **Assign to Agent Profile:** Even if a skill is enabled in the registry, the agent cannot see it until it is explicitly bound to the agent's profile.
   - In `~/.openclaw/openclaw.json`, locate the `agents.list` section.
   - Find your target agent (e.g., `"id": "main"`).
   - Add your skill's slug to the `"skills": []` array:
     ```json
     "agents": {
       "list": [
         {
           "id": "main",
           "skills": [
             "my-local-skill"
           ]
         }
       ]
     }
     ```
5. **Reload Session:** OpenClaw needs to reload its context. Restart your OpenClaw session or run `openclaw gateway restart` to apply changes.
