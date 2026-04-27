const plugin = require('/home/marku/.openclaw/extensions/google-workspace-plugin/dist/index.js');

async function run() {
    const api = {
        tools: {},
        registerTool: function(tool) {
            this.tools[tool.name] = tool;
        },
        on: function(event, callback) {
            if (event === 'plugin:ready') callback();
        }
    };
    
    plugin.default(api);
    
    const gogTool = api.tools['gog'];
    if (!gogTool) {
        console.error("gog tool not registered!");
        return;
    }
    
    try {
        const result = await gogTool.execute({ 
            action: "tasks.create", 
            body: { 
                title: "Alienware Jidoka Test Task", 
                notes: "Testing auto-correction of tasks.create hallucination" 
            } 
        });
        console.log(JSON.stringify(result, null, 2));
    } catch (e) {
        console.error("Test error:", e);
    }
}

run();
