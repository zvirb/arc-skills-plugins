import { PluginApi } from '@openclaw/plugin-sdk';

// Stub for Composio import.
let Composio: any = null;
try {
    Composio = require('composio').Composio;
} catch (e) {
    // Composio SDK not available
}

export const manifest = {
  name: "google-workspace-plugin",
  version: "1.0.0",
  configSchema: {
    type: "object",
    properties: {
      composioApiKey: { type: "string" }
    },
    required: ["composioApiKey"]
  }
};

// Sub-Agent: Context Preserver
// Spins up an isolated LLM inference loop to extract key entities from massive payloads, preventing context bloat for the parent agent.
async function summarizeWithSubAgent(api: PluginApi, data: any, actionContext: string): Promise<any> {
    const rawData = JSON.stringify(data);
    if (rawData.length < 1500) return data; // Safe size, no bloat risk

    console.log(`Payload size (${rawData.length} chars) exceeds safe threshold. Spawning sub-agent to preserve context...`);
    
    const systemPrompt = `You are an OpenClaw Context-Preservation Sub-Agent. 
TASK: Extract and summarize the critical entities from the raw JSON payload resulting from: ${actionContext}.
RULES:
1. Strip out verbose bodies, HTML, and irrelevant metadata.
2. Return ONLY a minified JSON array of key objects (e.g., id, title, brief_status).
3. Do not include markdown formatting or conversational text.`;

    try {
        const result = await api.infer({
            model: "gemma4", 
            messages: [{ role: "user", content: `${systemPrompt}\n\nRAW PAYLOAD:\n${rawData.substring(0, 8000)}` }]
        });
        
        const jsonStr = typeof result === 'string' ? result : result.content;
        const startIdx = jsonStr.indexOf('{');
        const arrayStartIdx = jsonStr.indexOf('[');
        const firstIdx = (startIdx !== -1 && arrayStartIdx !== -1) ? Math.min(startIdx, arrayStartIdx) : Math.max(startIdx, arrayStartIdx);
        
        const endIdx = jsonStr.lastIndexOf('}');
        const arrayEndIdx = jsonStr.lastIndexOf(']');
        const lastIdx = Math.max(endIdx, arrayEndIdx);
        
        if (firstIdx !== -1 && lastIdx !== -1) {
            const cleanJson = jsonStr.substring(firstIdx, lastIdx + 1);
            return { _sub_agent_summarized: true, original_length: rawData.length, data: JSON.parse(cleanJson) };
        }
    } catch (e: any) {
        console.log("Sub-agent summarization failed:", e.message);
    }
    
    // Fallback: Brutal truncation to preserve Jidoka stability
    return { _truncated: true, warning: "Data too large and sub-agent failed.", data: rawData.substring(0, 1500) + "...[TRUNCATED]" };
}

// Jidoka Loop for Google Workspace Execution (Native Node.js execution, NO subshells)
async function executeWorkspaceAction(api: PluginApi, composioApiKey: string, composioAction: string, args: Record<string, any>, maxRetries = 3): Promise<any> {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        console.log(`Attempt ${attempt}: Executing ${composioAction}...`);
        
        try {
            if (Composio && composioApiKey) {
                const client = new Composio({ apiKey: composioApiKey });
                const res = await client.tools.execute(composioAction, { arguments: args });
                if (res.successful) {
                    // Invoke Sub-Agent to prevent context bloat
                    const processedData = await summarizeWithSubAgent(api, res.data, composioAction);
                    return { success: true, data: processedData };
                }
            } else {
                 throw new Error("Composio SDK or API key missing.");
            }
        } catch (e: any) {
            console.log(`Composio failed on attempt ${attempt}:`, e.message);
        }
        
        console.log("Validation failed or tools errored. Retrying...");
        await new Promise(r => setTimeout(r, 2000));
    }
    
    throw new Error(`Failed to achieve expected outcome for ${composioAction} after ${maxRetries} retries.`);
}

export default function register(api: PluginApi, config: any) {
    const apiKey = config.composioApiKey;

    // Helper to register standard GWorkspace actions
    const registerWorkspaceTool = (name: string, description: string, composioCmd: string) => {
        api.registerTool({
            name,
            description,
            execute: async (args: any) => {
                try {
                    const result = await executeWorkspaceAction(api, apiKey, composioCmd, args);
                    return result;
                } catch (error: any) {
                    return { success: false, error: error.message };
                }
            }
        });
    };

    // Google Tasks
    registerWorkspaceTool('gworkspace_tasks_find', 'Find active tasks in Google Tasks.', 'GOOGLETASKS_LIST_TASKS');
    registerWorkspaceTool('gworkspace_tasks_update', 'Update a task in Google Tasks.', 'GOOGLETASKS_UPDATE_TASK');
    registerWorkspaceTool('gworkspace_tasks_create', 'Create a task in Google Tasks.', 'GOOGLETASKS_CREATE_TASK');
    registerWorkspaceTool('gworkspace_tasks_complete', 'Complete a task in Google Tasks.', 'GOOGLETASKS_COMPLETE_TASK');

    // Google Docs
    registerWorkspaceTool('gworkspace_docs_create', 'Create a Google Doc.', 'GOOGLEDOCS_CREATE_DOCUMENT');
    registerWorkspaceTool('gworkspace_docs_read', 'Read a Google Doc.', 'GOOGLEDOCS_READ_DOCUMENT');
    registerWorkspaceTool('gworkspace_docs_update', 'Update a Google Doc.', 'GOOGLEDOCS_UPDATE_DOCUMENT');

    // Google Drive
    registerWorkspaceTool('gworkspace_drive_search', 'Search for files in Google Drive.', 'GOOGLEDRIVE_SEARCH_FILES');
    registerWorkspaceTool('gworkspace_drive_upload', 'Upload a file to Google Drive.', 'GOOGLEDRIVE_UPLOAD_FILE');

    // Google Calendar
    registerWorkspaceTool('gworkspace_calendar_find', 'Find events in Google Calendar.', 'GOOGLECALENDAR_FIND_EVENT');
    registerWorkspaceTool('gworkspace_calendar_create', 'Create an event in Google Calendar.', 'GOOGLECALENDAR_CREATE_EVENT');

    api.on('plugin:ready', () => {
        console.log('GoogleWorkspace plugin loaded with native Jidoka tools.');
    });
}
