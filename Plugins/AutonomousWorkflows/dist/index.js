"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.manifest = void 0;
exports.default = register;
exports.manifest = {
    name: "autonomous-workflows-plugin",
    version: "1.0.0",
    dependencies: [
        "google-workspace-plugin",
        "llm-transformations-plugin"
    ]
};
function register(api) {
    api.registerTool({
        name: 'workflow_backlog_grooming',
        description: 'Autonomously identifies stale Google Tasks (30+ days old), summarizes them, prepends [STALE/ARCHIVED], and completes them.',
        execute: async (args) => {
            try {
                console.log("Workflow: Starting Backlog Grooming...");
                // 1. Fetch active tasks using the GoogleWorkspace plugin
                const findRes = await api.executeTool('gworkspace_tasks_find', {});
                if (!findRes.success || !findRes.data) {
                    return { success: false, message: "No active tasks found or failed to fetch." };
                }
                const tasks = findRes.data;
                const results = [];
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
                            const summaryData = await api.executeTool('llm_summarize_text', sumArgs);
                            if (summaryData.status === "error" || !summaryData.summary) {
                                throw new Error(summaryData.message || "Failed to summarize task");
                            }
                            const newTitle = `[STALE/ARCHIVED] ${summaryData.summary}`;
                            // 3. Update task
                            const updateArgs = {
                                id: task.id,
                                title: newTitle,
                                status: "completed"
                            };
                            const res = await api.executeTool('gworkspace_tasks_update', updateArgs);
                            if (res && res.success === false) {
                                throw new Error(res.error || "Failed to update task");
                            }
                            results.push(res);
                        }
                        catch (e) {
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
            catch (error) {
                return { success: false, error: error.message };
            }
        }
    });
    api.on('plugin:ready', () => {
        console.log('AutonomousWorkflows plugin loaded. Dependencies resolved.');
    });
}
