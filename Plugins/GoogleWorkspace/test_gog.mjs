import { gogHandler } from './dist/index.js';

async function run() {
    console.log("Testing gog handler...");
    try {
        const result = await gogHandler("tasks list");
        console.log("Result:", result);
    } catch (err) {
        console.error("Error:", err);
    }
}

run();
