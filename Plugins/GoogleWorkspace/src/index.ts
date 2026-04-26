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

// Jidoka Loop for Google Workspace Execution (Native Node.js execution, NO subshells)
async function executeWorkspaceAction(composioApiKey: string, composioAction: string, args: Record<string, any>, maxRetries = 3): Promise<any> {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        console.log(`Attempt ${attempt}: Executing ${composioAction}...`);
        
        try {
            if (Composio && composioApiKey) {
                const client = new Composio({ apiKey: composioApiKey });
                const res = await client.tools.execute(composioAction, { arguments: args });
                if (res.successful) {
                    return { success: true, data: res.data };
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
                    const result = await executeWorkspaceAction(apiKey, composioCmd, args);
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
