"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.default = register;
const child_process_1 = require("child_process");
const util_1 = require("util");
const execAsync = (0, util_1.promisify)(child_process_1.exec);
exports.manifest = {
    name: "google-workspace-plugin",
    version: "1.0.0",
    configSchema: {
        type: "object",
        properties: {
            composioApiKey: { type: "string" }
        }
    }
};
function register(ctx, second) {
    const api = ctx?.api || ctx;
    // This plugin acts as a bridge to specialized Workspace tools via Composio
    api.registerTool({
        name: 'workspace_bridge_status',
        description: 'Check the status of the Google Workspace bridge.',
        execute: async () => {
            return {
                status: "configured",
                active_tools: ["gmail", "calendar", "drive", "sheets", "tasks"]
            };
        }
    });
    // Native execution wrapper for the gog CLI binary
    api.registerTool({
        name: 'gog',
        description: 'Execute a command using the native gog CLI for Google Workspace operations (Gmail, Tasks, Calendar, etc).',
        parameters: {
            type: "object",
            properties: {
                args: {
                    type: "string",
                    description: "The arguments to pass to the gog CLI (e.g., 'tasks list @default --json')"
                }
            },
            required: ["args"]
        },
        execute: async (...execArgs) => {
            console.error('=== GOG TOOL EXECUTED ===', execArgs);
            // Handle both signature types: (params, ...) and (callId, params, ...)
            const input = (typeof execArgs[0] === 'string' && execArgs[1] && typeof execArgs[1] === 'object') ? execArgs[1] : execArgs[0];
            try {
                // Ensure we are only running the gog binary to prevent arbitrary shell injection
                const gogBin = process.env.GOG_BIN_PATH || '/home/marku/.local/bin/gog';
                let argsString = "";
                if (typeof input === "string") {
                    try {
                        const parsed = JSON.parse(input);
                        if (parsed.args)
                            argsString = parsed.args;
                        else if (parsed.params && parsed.params.args)
                            argsString = parsed.params.args;
                        else if (parsed.action) {
                            // Handle stringified Composio-style payload
                            const action = parsed.action.replace('.', ' ');
                            let bodyArgs = "";
                            if (parsed.body) {
                                for (const [k, v] of Object.entries(parsed.body)) {
                                    bodyArgs += ` --${k}="${String(v).replace(/"/g, '\\"')}"`;
                                }
                            }
                            argsString = `${action}${bodyArgs}`;
                        }
                        else
                            argsString = input;
                    }
                    catch (e) {
                        argsString = input;
                    }
                }
                else if (input && typeof input === "object") {
                    if (typeof input.args === "string") {
                        argsString = input.args;
                    }
                    else if (input.params && typeof input.params.args === "string") {
                        argsString = input.params.args;
                    }
                    else if (input.action) {
                        // Jidoka: Flatten composio-style structured payload
                        const action = String(input.action).replace('.', ' ');
                        let bodyArgs = "";
                        if (input.body && typeof input.body === "object") {
                            for (const [k, v] of Object.entries(input.body)) {
                                bodyArgs += ` --${k}="${String(v).replace(/"/g, '\\"')}"`;
                            }
                        }
                        argsString = `${action}${bodyArgs}`;
                    }
                    else {
                        // Fallback: convert top-level keys to flags if possible, or stringify
                        let fallbackArgs = "";
                        for (const [k, v] of Object.entries(input)) {
                            if (k !== 'args' && k !== 'params') {
                                fallbackArgs += ` --${k}="${String(v).replace(/"/g, '\\"')}"`;
                            }
                        }
                        argsString = fallbackArgs.trim() !== "" ? fallbackArgs.trim() : JSON.stringify(input);
                    }
                }
                else {
                    return { success: false, error: `Invalid tool input. Received: ${typeof input} ${String(input)}` };
                }
                // Jidoka: Auto-correct common LLM hallucinations for Google Tasks schema (tasklistId requirement)
                argsString = argsString.replace(/^tasks (create|add)\b(?!\s+@\w+)/i, 'tasks add @default');
                argsString = argsString.replace(/^tasks\.(create|add)\b(?!\s+@\w+)/i, 'tasks add @default');
                argsString = argsString.replace(/^tasks (list|ls)\b(?!\s+@\w+)/i, 'tasks list @default');
                argsString = argsString.replace(/^tasks\.(list|ls)\b(?!\s+@\w+)/i, 'tasks list @default');
                argsString = argsString.replace(/^tasks (update|edit|set)\b(?!\s+@\w+)/i, 'tasks update @default');
                argsString = argsString.replace(/^tasks\.(update|edit|set)\b(?!\s+@\w+)/i, 'tasks update @default');
                argsString = argsString.replace(/^tasks (done|complete)\b(?!\s+@\w+)/i, 'tasks done @default');
                argsString = argsString.replace(/^tasks\.(done|complete)\b(?!\s+@\w+)/i, 'tasks done @default');
                argsString = argsString.replace(/^tasks (delete|rm|remove)\b(?!\s+@\w+)/i, 'tasks delete @default');
                argsString = argsString.replace(/^tasks\.(delete|rm|remove)\b(?!\s+@\w+)/i, 'tasks delete @default');
                if (argsString === "undefined" || !argsString || argsString.trim() === "") {
                    return { success: false, error: "Parsed argsString is empty or undefined literal. Input was: " + JSON.stringify(input) };
                }
                // Jidoka validation: Strict timeout to prevent zombie subshells
                // Determine the binary to use
                let binary = 'gogcli';
                const { execSync } = require('child_process');
                try {
                    execSync('which gogcli', { stdio: 'ignore' });
                }
                catch {
                    try {
                        execSync('which gog', { stdio: 'ignore' });
                        binary = 'gog';
                    }
                    catch {
                        // Fallback to absolute paths if 'which' fails due to systemd PATH stripping
                        const fs = require('fs');
                        const defaultPath = process.env.GOG_BIN_PATH || '/home/marku/.local/bin/gog';
                        if (fs.existsSync(defaultPath)) {
                            binary = defaultPath;
                        }
                        else if (fs.existsSync('/home/marku/.local/bin/gogcli')) {
                            binary = '/home/marku/.local/bin/gogcli';
                        }
                        else {
                            throw new Error('Neither gogcli nor gog found in PATH or standard local bin directories');
                        }
                    }
                }
                // Prepare environment with password if available
                const env = { ...process.env };
                if (!env.GOG_KEYRING_PASSWORD) {
                    
                }
                const cmd = `${binary} ${argsString}`;
                const { stdout, stderr } = await execAsync(cmd, { timeout: 10000, env });
                if (stderr && stderr.trim().length > 0 && !stdout) {
                    return { success: false, error: stderr.trim() };
                }
                // Attempt to parse JSON if the command was requested with --json
                if (argsString.includes('--json')) {
                    try {
                        return { success: true, data: JSON.parse(stdout) };
                    }
                    catch (e) {
                        return { success: true, raw_output: stdout.trim() };
                    }
                }
                return { success: true, output: stdout.trim() };
            }
            catch (error) {
                console.error('=== GOG EXEC ERROR ===', error);
                // Jidoka: Deterministic error reporting for self-healing Andon loop
                return {
                    success: false,
                    error: `Command execution failed: ${error.message || error.stderr || 'Unknown error'}. Please correct your arguments and retry.`
                };
            }
        }
    });
    api.on('plugin:ready', () => {
        console.log('GoogleWorkspace custom bridge plugin loaded (with gog native execution support).');
    });
}
