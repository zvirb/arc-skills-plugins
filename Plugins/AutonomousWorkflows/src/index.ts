import { PluginApi } from '@openclaw/plugin-sdk';

export const manifest = {
  name: "autonomous-workflows-plugin",
  version: "1.0.0",
  dependencies: [
    "google-workspace-plugin",
    "llm-transformations-plugin"
  ]
};

export default function register(api: PluginApi) {

    api.registerTool({
        name: 'workflow_backlog_grooming',
        description: 'Autonomously identifies stale Google Tasks (30+ days old), summarizes them, prepends [STALE/ARCHIVED], and completes them.',
        execute: async () => {
            console.log("Workflow: Starting Backlog Grooming...");
            
            // 1. Fetch active tasks using the GoogleWorkspace plugin
            const findRes: any = await api.executeTool('gworkspace_tasks_find', {});
            if (!findRes.success || !findRes.data) {
                return { success: false, message: "No active tasks found or failed to fetch." };
            }
            
            const tasks = findRes.data;
            const results: any[] = [];
            const now = new Date();
            
            for (const task of tasks) {
                let isStale = false;
                if (task.updated) {
                    const updatedDt = new Date(task.updated);
                    const diffTime = Math.abs(now.getTime() - updatedDt.getTime());
                    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
                    if (diffDays > 30) {
                        isStale = true;
                    }
                }

                if (isStale) {
                    console.log(`Grooming stale task: '${task.title}'`);
                    
                    try {
                        // 2. Summarize via LLMTransformations plugin
                        const sumArgs = {
                            text: `${task.title} ${task.notes || ""}`,
                            schema: JSON.stringify({ summary: "string" })
                        };
                        const summaryData: any = await api.executeTool('llm_summarize_text', sumArgs);
                        
                        const newTitle = `[STALE/ARCHIVED] ${summaryData.summary}`;
                        
                        // 3. Update task
                        const updateArgs = {
                            id: task.id,
                            title: newTitle,
                            status: "completed"
                        };
                        const res = await api.executeTool('gworkspace_tasks_update', updateArgs);
                        results.push(res);
                    } catch (e: any) {
                        console.log(`Failed to groom task '${task.id}': ${e.message}`);
                    }
                }
            }
            
            return { 
                success: true, 
                total_groomed: results.length,
                sample_groomed: results.slice(0, 3)
            };
        }
    });

    api.on('plugin:ready', () => {
        console.log('AutonomousWorkflows plugin loaded. Dependencies resolved.');
    });
}
