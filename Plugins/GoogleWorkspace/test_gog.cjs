const plugin = require('./dist/index.js');

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
    
    console.log("Testing gog tool execute...");
    try {
        const result = await gogTool.execute({ args: "tasks list" });
        console.log("Result:", JSON.stringify(result, null, 2));
    } catch (e) {
        console.error("Test error:", e);
    }
}

run();
