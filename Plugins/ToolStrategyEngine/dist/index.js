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
        execute: async (args) => {
            const preferences = {
                "search": "exa_search",
                "mail": "gmail-send-email",
                "calendar": "google-calendar-create-event"
            };
            return { preferred_tool: preferences[args.category] || "unknown" };
        }
    });
    api.on('plugin:ready', () => {
        console.log('ToolStrategyEngine plugin loaded.');
    });
}
