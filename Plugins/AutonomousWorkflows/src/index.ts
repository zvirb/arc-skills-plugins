import { PluginApi } from '@openclaw/plugin-sdk';

export const manifest = {
  name: "autonomous-workflows-plugin",
  version: "1.0.0",
  description: "Programmatic deterministic workflows orchestrating atomic tools via TypeScript.",
  configSchema: {
    type: "object",
    properties: {}
  },
  dependencies: ["llm-transformations-plugin"]
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
                
                // Jidoka validation
                if (!searchResults || !searchResults.results || !Array.isArray(searchResults.results)) {
                     return { success: false, error: "exa_search failed to return valid results array. Please check the tool output and retry." };
                }

                // 2. Extract content from results
                const content = searchResults.results.map((r: any) => r.text).join('\n\n');
                
                if (!content) {
                     return { success: false, error: "Search results contained no text to summarize." };
                }

                // 3. Summarize via LLM Transformation
                return await api.callTool('llm_summarize_text', { text: content });
            } catch (error: any) {
                // Return structured Jidoka error
                return { success: false, error: `Workflow execution failed: ${error.message || 'Unknown error'}. Please correct and retry.` };
            }
        }
    });

    api.on('plugin:ready', () => {
        console.log('AutonomousWorkflows plugin loaded.');
    });
}
