---
name: LLM Extract JSON
description: Atomic transformation node to extract strictly formatted JSON from raw text using the LLMTransformations plugin.
os: windows
requires:
  plugins:
    - llm-transformations-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if JSON extraction fails.

# LLM Extract JSON

This skill allows the agent to extract structured JSON data from unstructured text.

## Cognitive Directives
WHEN [Raw text contains structured data that needs to be converted to JSON]
THEN [Execute the `llm_extract_json` plugin tool]

## Schema Example
```json
{
  "text": "The user is John Doe and he is 30 years old.",
  "schema": "{ 'name': 'string', 'age': 'number' }"
}
```

## Expected Output
A strictly formatted JSON object matching the requested schema.
