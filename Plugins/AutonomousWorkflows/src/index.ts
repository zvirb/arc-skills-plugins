import { PluginApi } from '@openclaw/plugin-sdk';

export const manifest = {
  name: "autonomous-workflows-plugin",
  version: "1.0.0",
  description: "Programmatic deterministic workflows orchestrating atomic tools via TypeScript.",
  configSchema: {
    type: "object",
    properties: {}
  }
};

export default function register(ctx: any, second: any) {
    const api: PluginApi = ctx?.api || ctx;
    const config = ctx?.pluginConfig || second || {};

    // Example Workflow: Research and Summarize
    api.registerTool({
        name: 'workflow_research_summarize',
        description: 'Autonomously research a topic and provide a structured summary.',
        execute: async (args: { topic: string }) => {
            try {
                // 1. Search for information
                const searchResults = await api.callTool('exa_search', { query: args.topic, num_results: 3 });
                
                // 2. Extract content from results
                const content = searchResults.results.map((r: any) => r.text).join('\n\n');
                
                // 3. Summarize via LLM Transformation
                return await api.callTool('llm_summarize_text', { text: content });
            } catch (error: any) {
                return { success: false, error: error.message };
            }
        }
    });

    api.on('plugin:ready', () => {
        console.log('AutonomousWorkflows plugin loaded.');
    });
}
