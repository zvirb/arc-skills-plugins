import { PluginApi } from '@openclaw/plugin-sdk';

export const manifest = {
  name: "llm-transformations-plugin",
  version: "1.0.0",
  configSchema: {
    type: "object",
    properties: {
      defaultModel: { type: "string", default: "gemma4" }
    }
  }
};

export default function register(ctx: any, second: any) {
    const api: PluginApi = ctx?.api || ctx;
    const config = ctx?.pluginConfig || second || {};
    const model = config?.defaultModel || "gemma4";

    // Standardized Jidoka Evaluator Loop for Atomic LLM Transformations (Native SDK implementation)
    async function executeWithJidoka(systemPrompt: string, payload: string, maxRetries: number = 3): Promise<any> {
        let errorFeedback = "";
        
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            const instruction = `${systemPrompt}\n\n${errorFeedback}\n\n${payload}`;
            try {
                // Atomic Execution (Native SDK inference)
                const result = await api.infer({
                    model: model,
                    messages: [{ role: "user", content: instruction }]
                });
                
                try {
                    // Evaluation - validate JSON
                    const jsonStr = typeof result === 'string' ? result : result.content;
                    const objStart = jsonStr.indexOf('{');
                    const arrStart = jsonStr.indexOf('[');
                    const startIdx = (objStart !== -1 && arrStart !== -1) ? Math.min(objStart, arrStart) : (objStart !== -1 ? objStart : arrStart);

                    const objEnd = jsonStr.lastIndexOf('}');
                    const arrEnd = jsonStr.lastIndexOf(']');
                    const endIdx = Math.max(objEnd, arrEnd);
                    
                    if (startIdx === -1 || endIdx === -1) {
                        throw new Error("No JSON object or array found in output.");
                    }
                    
                    const cleanJson = jsonStr.substring(startIdx, endIdx + 1);
                    const data = JSON.parse(cleanJson);
                    return data; // Success
                } catch (parseError) {
                    errorFeedback = `PREVIOUS_ERROR: Invalid JSON returned. ${parseError}. INSTRUCTION: Correct the JSON and try again.`;
                }
                
            } catch (error: any) {
                errorFeedback = `SYSTEM_EXCEPTION: ${error.message}`;
            }
            
            // Wait before retry
            await new Promise(r => setTimeout(r, 1000));
        }
        
        return {
            status: "error",
            message: `Failed to achieve valid state after ${maxRetries} attempts.`,
            last_error: errorFeedback
        };
    }

    // 1. LLM Summarize Text
    api.registerTool({
        name: 'llm_summarize_text',
        description: 'Summarize text into structured JSON.',
        parameters: {
            type: "object",
            properties: {
                text: { type: "string" },
                schema: { type: "string" }
            },
            required: ["text"]
        },
        execute: async (args: { text: string, schema?: string }) => {
            try {
                if (typeof args.text !== 'string') {
                    return { success: false, error: "Invalid argument: 'text' must be provided as a string. Please correct and retry." };
                }
                const rawText = args.text || "";
                const schemaHint = args.schema || JSON.stringify({ summary: "string", key_points: ["string"], sentiment: "string" });
                
                const systemPrompt = `ROLE: Data Transformation Node.\nTASK: Summarize text into structured JSON.\nSCHEMA: ${schemaHint}\nRULES: Output ONLY raw JSON. No conversational text. No markdown blocks.`;
                const currentPrompt = `TEXT TO PROCESS: ${rawText.substring(0, 3000)}`;
                
                return await executeWithJidoka(systemPrompt, currentPrompt);
            } catch (error: any) {
                return { success: false, error: error.message };
            }
        }
    });

    // 2. LLM Extract JSON
    api.registerTool({
        name: 'llm_extract_json',
        description: 'Extract raw JSON from unstructured text.',
        parameters: {
            type: "object",
            properties: {
                text: { type: "string" },
                expected_schema: { type: "string" }
            },
            required: ["text"]
        },
        execute: async (args: { text: string, expected_schema?: string }) => {
            try {
                if (typeof args.text !== 'string') {
                    return { success: false, error: "Invalid argument: 'text' must be provided as a string. Please correct and retry." };
                }
                const rawText = args.text || "";
                const schemaHint = args.expected_schema || "Any JSON object or array.";
                
                const systemPrompt = `ROLE: Data Extraction Node.\nTASK: Extract JSON from text.\nSCHEMA: ${schemaHint}\nRULES: Output ONLY raw JSON. No markdown blocks.`;
                const currentPrompt = `TEXT TO PROCESS: ${rawText.substring(0, 5000)}`;
                
                return await executeWithJidoka(systemPrompt, currentPrompt);
            } catch (error: any) {
                return { success: false, error: error.message };
            }
        }
    });

    // 3. LLM Classify Intent
    api.registerTool({
        name: 'llm_classify_intent',
        description: 'Classify the intent of a text payload.',
        parameters: {
            type: "object",
            properties: {
                text: { type: "string" },
                categories: { type: "array", items: { type: "string" } }
            },
            required: ["text", "categories"]
        },
        execute: async (args: { text: string, categories: string[] }) => {
            try {
                if (!args.categories || !Array.isArray(args.categories)) {
                    return { success: false, error: "Invalid argument: 'categories' must be provided as an array. Please correct and retry." };
                }
                const rawText = args.text || "";
                const categories = args.categories.join(', ');
                
                const systemPrompt = `ROLE: Classification Node.\nTASK: Classify the input text into one of the following categories: ${categories}.\nSCHEMA: {"intent": "string", "confidence": "number"}\nRULES: Output ONLY raw JSON.`;
                const currentPrompt = `TEXT TO PROCESS: ${rawText}`;
                
                return await executeWithJidoka(systemPrompt, currentPrompt);
            } catch (error: any) {
                return { success: false, error: error.message };
            }
        }
    });

    api.on('plugin:ready', () => {
        console.log('LLMTransformations plugin loaded with atomic SDK-native Jidoka tools.');
    });
}
