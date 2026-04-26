import { PluginApi } from '@openclaw/plugin-sdk';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Stub for Composio import. In a real environment, you'd add composio-core to package.json dependencies.
let Composio: any = null;
try {
    Composio = require('composio').Composio;
} catch (e) {
    // Composio SDK not available
}

// Jidoka Loop for Google Workspace Execution
async function executeWorkspaceAction(gogCommand: string, composioAction: string, args: Record<string, any>, maxRetries = 3): Promise<any> {
    const composioApiKey = process.env.COMPOSIO_API_KEY;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        console.log(`Attempt ${attempt}: Executing ${composioAction}...`);
        
        // 1. Try native 'gog'
        try {
            const cliArgs = Object.entries(args).map(([k, v]) => `--${k}='${v}'`).join(' ');
            const cmd = `wsl -- bash -c "gog ${gogCommand} ${cliArgs} --json"`;
            const { stdout } = await execAsync(cmd);
            const data = JSON.parse(stdout);
            return { success: true, data };
        } catch (e: any) {
            console.log(`gog tool failed on attempt ${attempt}:`, e.message);
        }
        
        // 2. Try Composio fallback
        try {
            if (Composio && composioApiKey) {
                const client = new Composio({ apiKey: composioApiKey });
                const res = await client.tools.execute(composioAction, { arguments: args });
                if (res.successful) {
                    return { success: true, data: res.data };
                }
            }
        } catch (e: any) {
            console.log(`Fallback composio failed on attempt ${attempt}:`, e.message);
        }
        
        console.log("Validation failed or tools errored. Retrying...");
        await new Promise(r => setTimeout(r, 2000));
    }
    
    throw new Error(`Failed to achieve expected outcome for ${composioAction} after ${maxRetries} retries.`);
}

export default function register(api: PluginApi) {

    // Helper to register standard GWorkspace actions
    const registerWorkspaceTool = (name: string, description: string, gogCmd: string, composioCmd: string) => {
        api.registerTool({
            name,
            description,
            execute: async (args: any) => {
                try {
                    const result = await executeWorkspaceAction(gogCmd, composioCmd, args);
                    return result;
                } catch (error: any) {
                    return { success: false, error: error.message };
                }
            }
        });
    };

    // Google Tasks
    registerWorkspaceTool('gworkspace_tasks_find', 'Find active tasks in Google Tasks.', 'tasks list', 'GOOGLETASKS_LIST_TASKS');
    registerWorkspaceTool('gworkspace_tasks_update', 'Update a task in Google Tasks.', 'tasks update', 'GOOGLETASKS_UPDATE_TASK');
    registerWorkspaceTool('gworkspace_tasks_create', 'Create a task in Google Tasks.', 'tasks create', 'GOOGLETASKS_CREATE_TASK');
    registerWorkspaceTool('gworkspace_tasks_complete', 'Complete a task in Google Tasks.', 'tasks complete', 'GOOGLETASKS_COMPLETE_TASK');

    // Google Docs
    registerWorkspaceTool('gworkspace_docs_create', 'Create a Google Doc.', 'docs create', 'GOOGLEDOCS_CREATE_DOCUMENT');
    registerWorkspaceTool('gworkspace_docs_read', 'Read a Google Doc.', 'docs read', 'GOOGLEDOCS_READ_DOCUMENT');
    registerWorkspaceTool('gworkspace_docs_update', 'Update a Google Doc.', 'docs update', 'GOOGLEDOCS_UPDATE_DOCUMENT');

    // Google Drive
    registerWorkspaceTool('gworkspace_drive_search', 'Search for files in Google Drive.', 'drive search', 'GOOGLEDRIVE_SEARCH_FILES');
    registerWorkspaceTool('gworkspace_drive_upload', 'Upload a file to Google Drive.', 'drive upload', 'GOOGLEDRIVE_UPLOAD_FILE');

    // Google Calendar
    registerWorkspaceTool('gworkspace_calendar_find', 'Find events in Google Calendar.', 'calendar find', 'GOOGLECALENDAR_FIND_EVENT');
    registerWorkspaceTool('gworkspace_calendar_create', 'Create an event in Google Calendar.', 'calendar create', 'GOOGLECALENDAR_CREATE_EVENT');

    api.on('plugin:ready', () => {
        console.log('GoogleWorkspace plugin loaded with resilient fallback tools.');
    });
}
