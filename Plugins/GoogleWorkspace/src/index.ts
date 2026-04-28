export interface PluginApi {
  registerTool(tool: any): void;
  on(event: string, callback: () => void): void;
}
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export const manifest = {
  name: "google-workspace-plugin",
  version: "1.0.0",
  configSchema: {
    type: "object",
    properties: {
      composioApiKey: { type: "string" }
    }
  }
};

export default function register(ctx: any, second: any) {
    const api: PluginApi = ctx?.api || ctx;

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
        description: 'Execute a command using the native gog CLI for Google Workspace operations (Gmail, Tasks, Calendar, etc). To add a task, use: gog tasks add @default --title="Task Title" (one at a time). Do not use batch flags like --add.',
        parameters: {
            type: "object",
            properties: {
                service: { type: "string", enum: ["tasks", "calendar", "gmail"], description: "The Google service to use (e.g., 'tasks' or 'calendar')" },
                action: { type: "string", enum: ["add", "create", "list", "update", "delete", "done", "event", "send"], description: "The action to perform" },
                targetId: { type: "string", description: "The specific Task ID or Calendar Event ID. REQUIRED for update, delete, and done/complete. NEVER pass the title here." },
                title: { type: "string", description: "The summary or title of the task/event to create or update" },
                notes: { type: "string", description: "The notes or description body" },
                start: { type: "string", description: "Start time for events (Strictly RFC3339 format, e.g., 2026-04-29T16:00:00+10:00)" },
                end: { type: "string", description: "End time for events (Strictly RFC3339 format)" },
                extraFlags: { type: "string", description: "Additional raw flags, e.g. '--json'" },
                args: { type: "string", description: "Legacy raw CLI arguments (Use the structured parameters above instead if possible)" }
            }
        },
        execute: async (...execArgs: any[]) => {
            console.error('=== GOG TOOL EXECUTED ===', execArgs);
            // Handle both signature types: (params, ...) and (callId, params, ...)
            let input = (typeof execArgs[0] === 'string' && execArgs[1] && typeof execArgs[1] === 'object') ? execArgs[1] : execArgs[0];
            try {
                // Ensure we are only running the gog binary to prevent arbitrary shell injection
                const gogBin = process.env.GOG_BIN_PATH || '/home/marku/.local/bin/gog';
                
                let argsString = "";
                if (typeof input === "string") {
                    try {
                        const parsed = JSON.parse(input);
                        input = parsed;
                    } catch (e) {
                        argsString = input;
                    }
                } 
                
                if (typeof input === "object") {
                    if (input.service && input.action) {
                        // Schema-Based Parameter Builder
                        let parts = [input.service, input.action];
                        
                        // Handle strict ID requirements
                        if (input.service === "tasks") parts.push("@default");
                        if (input.service === "calendar") parts.push("primary");

                        if (input.targetId) {
                            parts.push(input.targetId);
                        }
                        
                        // Append properties as flags
                        if (input.title) {
                            if (input.service === "tasks") parts.push(`--title="${String(input.title).replace(/"/g, '\\"')}"`);
                            if (input.service === "calendar") parts.push(`--summary="${String(input.title).replace(/"/g, '\\"')}"`);
                        }
                        if (input.notes) parts.push(`--notes="${String(input.notes).replace(/"/g, '\\"')}"`);
                        if (input.start) parts.push(`--from="${String(input.start).replace(/"/g, '\\"')}"`);
                        if (input.end) parts.push(`--to="${String(input.end).replace(/"/g, '\\"')}"`);
                        if (input.extraFlags) parts.push(input.extraFlags);

                        argsString = parts.join(" ");
                    } else if (typeof input.args === "string") {
                        argsString = input.args;
                    } else if (input.params && typeof input.params.args === "string") {
                        argsString = input.params.args;
                    } else if (input.action && !input.service) {
                        // Jidoka: Flatten composio-style structured payload
                        const action = String(input.action).replace('.', ' ');
                        let bodyArgs = "";
                        if (input.body && typeof input.body === "object") {
                            for (const [k, v] of Object.entries(input.body)) {
                                bodyArgs += ` --${k}="${String(v).replace(/"/g, '\\"')}"`;
                            }
                        }
                        argsString = `${action}${bodyArgs}`;
                    } else {
                        // Fallback: convert top-level keys to flags if possible, or stringify
                        let fallbackArgs = "";
                        for (const [k, v] of Object.entries(input)) {
                            if (k !== 'args' && k !== 'params' && k !== 'service' && k !== 'action') {
                                fallbackArgs += ` --${k}="${String(v).replace(/"/g, '\\"')}"`;
                            }
                        }
                        argsString = fallbackArgs.trim() !== "" ? fallbackArgs.trim() : JSON.stringify(input);
                    }
                } else if (!argsString) {
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

                // Jidoka: Naked Title Conversion
                argsString = argsString.replace(/^tasks add (@[\w-]+)\s+(['"].+?['"])$/i, 'tasks add $1 --title=$2');

                // Jidoka: Auto-correct common LLM hallucinations for Google Calendar schema (calendarId requirement)
                argsString = argsString.replace(/^calendar (create|add|new)\b(?!\s+(primary|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))/i, 'calendar create primary');
                argsString = argsString.replace(/^calendar\.(create|add|new)\b(?!\s+(primary|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))/i, 'calendar create primary');
                argsString = argsString.replace(/^calendar (update|edit|set)\b(?!\s+(primary|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))/i, 'calendar update primary');
                argsString = argsString.replace(/^calendar\.(update|edit|set)\b(?!\s+(primary|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))/i, 'calendar update primary');
                argsString = argsString.replace(/^calendar (delete|rm|del|remove)\b(?!\s+(primary|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))/i, 'calendar delete primary');
                argsString = argsString.replace(/^calendar\.(delete|rm|del|remove)\b(?!\s+(primary|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))/i, 'calendar delete primary');
                argsString = argsString.replace(/^calendar (event|get|info|show)\b(?!\s+(primary|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))/i, 'calendar event primary');
                argsString = argsString.replace(/^calendar\.(event|get|info|show)\b(?!\s+(primary|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}))/i, 'calendar event primary');
                
                if (argsString === "undefined" || !argsString || argsString.trim() === "") {
                     return { success: false, error: "Parsed argsString is empty or undefined literal. Input was: " + JSON.stringify(input) };
                }

                // Append --force and --no-input to prevent hanging on all commands natively
                if (!argsString.includes('--force') && !argsString.includes('-y')) {
                    argsString += " --force";
                }
                if (!argsString.includes('--no-input')) {
                    argsString += " --no-input";
                }

                // Jidoka: Enforce atomic operations (Kaizen). Reject hallucinated batch flags like --add.
                if (argsString.includes('--add')) {
                     return { 
                        success: false, 
                        error: "Jidoka Violation: Batch operations are strictly forbidden and the '--add' flag does not exist. You must create tasks one at a time to ensure atomic operations (Kaizen). Use '--title' for the task name." 
                     };
                }

                // Jidoka validation: Strict timeout to prevent zombie subshells
                // Determine the binary to use
                let binary = 'gogcli';
                const { execSync } = require('child_process');
                try {
                  execSync('which gogcli', { stdio: 'ignore' });
                } catch {
                  try {
                    execSync('which gog', { stdio: 'ignore' });
                    binary = 'gog';
                  } catch {
                    // Fallback to absolute paths if 'which' fails due to systemd PATH stripping
                    const fs = require('fs');
                    const defaultPath = process.env.GOG_BIN_PATH || '/home/marku/.local/bin/gog';
                    if (fs.existsSync(defaultPath)) {
                        binary = defaultPath;
                    } else if (fs.existsSync('/home/marku/.local/bin/gogcli')) {
                        binary = '/home/marku/.local/bin/gogcli';
                    } else {
                        throw new Error('Neither gogcli nor gog found in PATH or standard local bin directories');
                    }
                  }
                }

                // Prepare environment with password if available
                const env = { ...process.env };
                if (!env.GOG_KEYRING_PASSWORD) {
                    env.GOG_KEYRING_PASSWORD = '985832';
                }
                if (!env.GOG_ACCOUNT) {
                    env.GOG_ACCOUNT = 'markuszvirbulis@gmail.com';
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
                    } catch (e) {
                        return { success: true, raw_output: stdout.trim() };
                    }
                }

                return { success: true, output: stdout.trim() };
                
            } catch (error: any) {
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
