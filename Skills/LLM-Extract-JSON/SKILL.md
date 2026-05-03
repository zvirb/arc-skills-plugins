---
name: kebab-case-auto-fix
description: Atomic node to extract strictly formatted JSON from raw text.
---

# LLM Extract JSON

This skill directs the agent to extract structured data from unstructured text using a provided schema.

## Execution Directives
1. **Define Schema:** Establish the target JSON schema (e.g., `{ "name": "string", "date": "string" }`).
2. **Execute Extraction:** Run the `llm_extract_json` tool with the raw text and schema.
3. **Verify Validity:** Parse the resulting JSON. If it is invalid or does not match the schema, re-prompt the tool with the error message.
4. **Finalize Output:** Return the verified JSON object.

## Expected Output
A strictly formatted JSON object matching the requested schema.
