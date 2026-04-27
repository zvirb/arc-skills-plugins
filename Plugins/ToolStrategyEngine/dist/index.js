"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.default = register;
exports.manifest = {
    name: "tool-strategy-engine",
    version: "1.0.0",
    configSchema: {
        type: "object",
        properties: {
            storageKey: { type: "string", default: "tool_strategy_default" }
        }
    }
};
function register(ctx, second) {
    const api = ctx?.api || ctx;
    const config = ctx?.pluginConfig || second || {};
    const storageKey = config?.storageKey || "tool_strategy_default";
    api.registerTool({
        name: 'strategy_get_preference',
        description: 'Get the preferred tool for a specific task category.',
        parameters: {
            type: "object",
            properties: {
                category: { type: "string" }
            },
            required: ["category"]
        },
        execute: async (args) => {
            try {
                if (typeof args.category !== 'string') {
                    return { success: false, error: "Invalid argument: 'category' must be provided as a string. Please correct and retry." };
                }
                const preferences = {
                    "search": "exa_search",
                    "mail": "gmail-send-email",
                    "calendar": "google-calendar-create-event"
                };
                return { preferred_tool: preferences[args.category] || "unknown" };
            }
            catch (error) {
                return { success: false, error: `ToolStrategyEngine failed: ${error.message || 'Unknown error'}. Please correct and retry.` };
            }
        }
    });
    api.on('plugin:ready', () => {
        console.log('ToolStrategyEngine plugin loaded.');
    });
}
