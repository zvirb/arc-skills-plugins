import { PluginApi } from '@openclaw/plugin-sdk';

// Define the schema for the history file
interface ToolConstraint {
  known_errors: string[];
  argument_rules: string[];
}

interface ToolHistory {
  use_cases: Record<string, {
    successful_tools: string[];
    anti_patterns: string[];
  }>;
  tool_constraints: Record<string, ToolConstraint>;
}

// Exported manifest defining the plugin structure (Anti-pattern fix: Manifest & ConfigSchema)
export const manifest = {
  name: "tool-strategy-engine",
  version: "1.0.0",
  configSchema: {
    type: "object",
    properties: {
      storageKey: { type: "string", default: "tool_history" }
    }
  }
};

export default function register(api: PluginApi, config: any) {
  const storageKey = config.storageKey || "tool_history";

  // Ensure memory directory exists and load history securely (Anti-pattern fix: Native Storage API)
  async function loadHistory(): Promise<ToolHistory> {
    try {
      const data = await api.storage.get(storageKey);
      return data || { use_cases: {}, tool_constraints: {} };
    } catch (error) {
      console.error('Failed to load tool history from storage:', error);
      return { use_cases: {}, tool_constraints: {} };
    }
  }

  async function saveHistory(history: ToolHistory): Promise<void> {
    try {
      await api.storage.set(storageKey, history);
    } catch (error) {
      console.error('Failed to save tool history to storage:', error);
    }
  }

  // Tool: Get Tool Constraints
  api.registerTool({
    name: 'get_tool_constraints',
    description: 'Retrieves historical constraints and known anti-patterns for specified tools to prevent hallucination.',
    execute: async (args: { tools: string[] }) => {
      const history = await loadHistory();
      const constraints: Record<string, ToolConstraint> = {};
      
      for (const tool of args.tools) {
        if (history.tool_constraints[tool]) {
          constraints[tool] = history.tool_constraints[tool];
        } else {
          constraints[tool] = { known_errors: [], argument_rules: [] };
        }
      }
      return { success: true, constraints };
    }
  });

  // Tool: Record Tool Failure
  api.registerTool({
    name: 'record_tool_failure',
    description: 'Records a failure for a specific tool to build the historical ledger and prevent future hallucinations.',
    execute: async (args: { tool_name: string, error_encountered: string, argument_rule: string }) => {
      const history = await loadHistory();
      const tool = args.tool_name;

      if (!history.tool_constraints[tool]) {
        history.tool_constraints[tool] = { known_errors: [], argument_rules: [] };
      }

      if (args.error_encountered && !history.tool_constraints[tool].known_errors.includes(args.error_encountered)) {
        history.tool_constraints[tool].known_errors.push(args.error_encountered);
        if (history.tool_constraints[tool].known_errors.length > 5) {
            history.tool_constraints[tool].known_errors.shift(); // Keep only last 5
        }
      }
      
      if (args.argument_rule && !history.tool_constraints[tool].argument_rules.includes(args.argument_rule)) {
        history.tool_constraints[tool].argument_rules.push(args.argument_rule);
        if (history.tool_constraints[tool].argument_rules.length > 5) {
            history.tool_constraints[tool].argument_rules.shift(); // Keep only last 5
        }
      }

      await saveHistory(history);
      return { success: true, message: `Successfully recorded constraints for ${tool}.` };
    }
  });

  api.on('plugin:ready', () => {
    console.log('ToolStrategyEngine plugin is ready (using secure storage api).');
  });
}
