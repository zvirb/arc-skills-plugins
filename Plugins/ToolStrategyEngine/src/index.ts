import { PluginApi } from '@openclaw/plugin-sdk';
import * as fs from 'fs';
import * as path from 'path';

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

const HISTORY_FILE_PATH = path.join(__dirname, '../../../../Memory/tool_history.json');

// Ensure memory directory exists and load history
function loadHistory(): ToolHistory {
  try {
    if (!fs.existsSync(HISTORY_FILE_PATH)) {
      const dir = path.dirname(HISTORY_FILE_PATH);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      const initialHistory: ToolHistory = { use_cases: {}, tool_constraints: {} };
      fs.writeFileSync(HISTORY_FILE_PATH, JSON.stringify(initialHistory, null, 2), 'utf-8');
      return initialHistory;
    }
    const data = fs.readFileSync(HISTORY_FILE_PATH, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Failed to load tool history:', error);
    return { use_cases: {}, tool_constraints: {} };
  }
}

function saveHistory(history: ToolHistory): void {
  try {
    fs.writeFileSync(HISTORY_FILE_PATH, JSON.stringify(history, null, 2), 'utf-8');
  } catch (error) {
    console.error('Failed to save tool history:', error);
  }
}

export default function register(api: PluginApi) {
  // Tool: Get Tool Constraints
  api.registerTool({
    name: 'get_tool_constraints',
    description: 'Retrieves historical constraints and known anti-patterns for specified tools to prevent hallucination.',
    execute: async (args: { tools: string[] }) => {
      const history = loadHistory();
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
      const history = loadHistory();
      const tool = args.tool_name;

      if (!history.tool_constraints[tool]) {
        history.tool_constraints[tool] = { known_errors: [], argument_rules: [] };
      }

      if (args.error_encountered && !history.tool_constraints[tool].known_errors.includes(args.error_encountered)) {
        history.tool_constraints[tool].known_errors.push(args.error_encountered);
      }
      
      if (args.argument_rule && !history.tool_constraints[tool].argument_rules.includes(args.argument_rule)) {
        history.tool_constraints[tool].argument_rules.push(args.argument_rule);
      }

      saveHistory(history);
      return { success: true, message: `Successfully recorded constraints for ${tool}.` };
    }
  });

  api.on('plugin:ready', () => {
    console.log('ToolStrategyEngine plugin is ready.');
  });
}
