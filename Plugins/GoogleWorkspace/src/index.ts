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
  version: "1.1.0",
  configSchema: {
    type: "object",
    properties: {
      composioApiKey: { type: "string" },
      subAgentModel: { type: "string", default: "gemma4" }
    },
    required: ["composioApiKey"]
  }
};

/**
 * Sub-Agent: Context Preserver
 * Spins up an isolated LLM inference loop to extract key entities from massive payloads.
 */
async function summarizeWithSubAgent(api: PluginApi, data: any, actionContext: string, model: string): Promise<any> {
    const rawData = JSON.stringify(data);
    if (rawData.length < 1500) return data; 

    console.log(`Payload size (${rawData.length} chars) exceeds safe threshold. Spawning sub-agent [${model}] to preserve context...`);
    
    const systemPrompt = `You are an OpenClaw Context-Preservation Sub-Agent. 
TASK: Extract and summarize the critical entities from the raw JSON payload resulting from: ${actionContext}.
RULES:
1. Strip out verbose bodies, HTML, and irrelevant metadata.
2. Return ONLY a minified JSON array of key objects (e.g., id, title, brief_status).
3. Do not include markdown formatting or conversational text.`;

    try {
        const result = await api.infer({
            model: model, 
            messages: [{ role: "user", content: `${systemPrompt}\n\nRAW PAYLOAD:\n${rawData.substring(0, 8000)}` }]
        });
        
        const jsonStr = typeof result === 'string' ? result : result.content;
        const startIdx = jsonStr.indexOf('[');
        const objStartIdx = jsonStr.indexOf('{');
        const firstIdx = (startIdx !== -1 && objStartIdx !== -1) ? Math.min(startIdx, objStartIdx) : (startIdx !== -1 ? startIdx : objStartIdx);
        
        const endIdx = jsonStr.lastIndexOf(']');
        const objEndIdx = jsonStr.lastIndexOf('}');
        const lastIdx = Math.max(endIdx, objEndIdx);
        
        if (firstIdx !== -1 && lastIdx !== -1) {
            const cleanJson = jsonStr.substring(firstIdx, lastIdx + 1);
            return { _sub_agent_summarized: true, original_length: rawData.length, data: JSON.parse(cleanJson) };
        }
    } catch (e: any) {
        console.log("Sub-agent summarization failed:", e.message);
    }
    
    return { _truncated: true, warning: "Data too large and sub-agent failed.", data: rawData.substring(0, 1500) + "...[TRUNCATED]" };
}

/**
 * Jidoka Loop for Google Workspace Execution
 */
async function executeWorkspaceAction(api: PluginApi, composioApiKey: string, composioAction: string, args: Record<string, any>, model: string, maxRetries = 3): Promise<any> {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            if (!Composio || !composioApiKey) {
                 throw new Error("Composio SDK or API key missing.");
            }

            const client = new Composio({ apiKey: composioApiKey });
            const res = await client.tools.execute(composioAction, { arguments: args });
            
            if (res.successful) {
                const processedData = await summarizeWithSubAgent(api, res.data, composioAction, model);
                return { success: true, data: processedData };
            } else {
                // If the tool specifically returned a failure message, we treat it as an error to trigger the retry/catch
                throw new Error(res.error || "Action failed without specific error message.");
            }
        } catch (e: any) {
            console.log(`Composio failed on attempt ${attempt} for ${composioAction}:`, e.message);
            if (attempt === maxRetries) {
                return { success: false, error: `Failed after ${maxRetries} retries: ${e.message}` };
            }
            await new Promise(r => setTimeout(r, 1000 * attempt)); // Exponential-ish backoff
        }
    }
}

export default function register(api: PluginApi, config: any) {
    const apiKey = config.composioApiKey;
    const model = config.subAgentModel;

    const registerWorkspaceTool = (name: string, description: string, composioCmd: string) => {
        api.registerTool({
            name,
            description,
            execute: async (args: any) => {
                return await executeWorkspaceAction(api, apiKey, composioCmd, args, model);
            }
        });
    };

    // Gmail Tools
    registerWorkspaceTool('gworkspace_gmail_search', 'Search for emails in Gmail.', 'GMAIL_SEARCH_EMAILS');
    registerWorkspaceTool('gworkspace_gmail_retrieve', 'Retrieve the full content of an email.', 'GMAIL_GET_EMAIL');
    registerWorkspaceTool('gworkspace_gmail_send', 'Send a new email.', 'GMAIL_SEND_EMAIL');
    registerWorkspaceTool('gworkspace_gmail_draft', 'Create a draft email.', 'GMAIL_CREATE_DRAFT');
    registerWorkspaceTool('gworkspace_gmail_delete', 'Delete an email.', 'GMAIL_DELETE_EMAIL');
    registerWorkspaceTool('gworkspace_gmail_modify_labels', 'Modify labels on an email.', 'GMAIL_BATCH_MODIFY_LABELS');

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
    registerWorkspaceTool('gworkspace_drive_delete', 'Delete a file from Google Drive.', 'GOOGLEDRIVE_DELETE_FILE');
    registerWorkspaceTool('gworkspace_drive_download', 'Download a file from Google Drive.', 'GOOGLEDRIVE_DOWNLOAD_FILE');
    registerWorkspaceTool('gworkspace_drive_share', 'Share a file in Google Drive.', 'GOOGLEDRIVE_SHARE_FILE');

    // Google Sheets
    registerWorkspaceTool('gworkspace_sheets_create', 'Create a new Google Spreadsheet.', 'GOOGLESHEETS_CREATE_SPREADSHEET');
    registerWorkspaceTool('gworkspace_sheets_append', 'Append a row to a Google Sheet.', 'GOOGLESHEETS_APPEND_ROW');
    registerWorkspaceTool('gworkspace_sheets_read', 'Read a range from a Google Sheet.', 'GOOGLESHEETS_READ_RANGE');
    registerWorkspaceTool('gworkspace_sheets_update', 'Update a range in a Google Sheet.', 'GOOGLESHEETS_UPDATE_RANGE');

    // Google Calendar
    registerWorkspaceTool('gworkspace_calendar_find', 'Find events in Google Calendar.', 'GOOGLECALENDAR_FIND_EVENT');
    registerWorkspaceTool('gworkspace_calendar_create', 'Create an event in Google Calendar.', 'GOOGLECALENDAR_CREATE_EVENT');
    registerWorkspaceTool('gworkspace_calendar_update', 'Update an event in Google Calendar.', 'GOOGLECALENDAR_UPDATE_EVENT');
    registerWorkspaceTool('gworkspace_calendar_delete', 'Delete an event in Google Calendar.', 'GOOGLECALENDAR_DELETE_EVENT');

    api.on('plugin:ready', () => {
        console.log('GoogleWorkspace plugin v1.1.0 loaded with expanded Gmail and Calendar tools.');
    });
}

