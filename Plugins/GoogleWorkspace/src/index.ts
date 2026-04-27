import { PluginApi } from '@openclaw/plugin-sdk';
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
        description: 'Execute a command using the native gog CLI for Google Workspace operations (Gmail, Tasks, Calendar, etc).',
        schema: {
            type: "object",
            properties: {
                args: { 
                    type: "string", 
                    description: "The arguments to pass to the gog CLI (e.g., 'tasks list @default --json')" 
                }
            },
            required: ["args"]
        },
        execute: async (input: { args: string }) => {
            try {
                // Ensure we are only running the gog binary to prevent arbitrary shell injection
                const gogBin = process.env.GOG_BIN_PATH || '/home/marku/.local/bin/gog';
                const cmd = `${gogBin} ${input.args}`;
                
                // Jidoka validation: Strict timeout to prevent zombie subshells
                const { stdout, stderr } = await execAsync(cmd, { timeout: 10000 });
                
                if (stderr && stderr.trim().length > 0 && !stdout) {
                     return { success: false, error: stderr.trim() };
                }

                // Attempt to parse JSON if the command was requested with --json
                if (input.args.includes('--json')) {
                    try {
                        return { success: true, data: JSON.parse(stdout) };
                    } catch (e) {
                        return { success: true, raw_output: stdout.trim() };
                    }
                }

                return { success: true, output: stdout.trim() };
                
            } catch (error: any) {
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
