import { PluginApi } from '@openclaw/plugin-sdk';

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
    const config = ctx?.pluginConfig || second || {};
    const composioApiKey = config?.composioApiKey;

    // This plugin acts as a bridge to specialized Workspace tools via Composio
    api.registerTool({
        name: 'workspace_bridge_status',
        description: 'Check the status of the Google Workspace bridge.',
        execute: async () => {
            return { 
                status: composioApiKey ? "configured" : "missing_api_key",
                active_tools: ["gmail", "calendar", "drive", "sheets"]
            };
        }
    });

    api.on('plugin:ready', () => {
        console.log('GoogleWorkspace custom bridge plugin loaded.');
    });
}
