---
name: llm-classify-intent
description: Atomic node to classify the intent and urgency of text.
---

# LLM Classify Intent

This skill directs the agent to perform semantic classification on a provided text snippet.

## Execution Directives
1. **Define Categories:** Establish the target categories (e.g., `Actionable`, `Informational`, `Urgent`).
2. **Execute Classification:** Execute the `llm_classify_intent` tool with the text and categories JSON.
3. **Verify Output:** Ensure the tool returns exactly one of the requested categories and an urgency level (`High`, `Medium`, `Low`).
4. **Handle Hallucinations:** If the output contains categories not in the allowed list, re-prompt the model to select from the provided list.
5. **Report Result:** Return the final classification JSON to the caller.

## Expected Output
A JSON object: `{ "intent": "string", "urgency": "string", "reasoning": "string" }`.
