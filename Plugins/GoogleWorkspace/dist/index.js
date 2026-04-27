"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.default = register;
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
