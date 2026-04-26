---
name: LLM Summarize Text
description: Atomic transformation node to summarize raw text using the LLMTransformations plugin.
os: windows
requires:
  plugins:
    - llm-transformations-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if summarization fails.

# LLM Summarize Text

This skill allows the agent to generate concise summaries of long text.

## Cognitive Directives
WHEN [Long text needs to be condensed into a brief summary]
THEN [Execute the `llm_summarize_text` plugin tool]

## Schema Example
```json
{
  "text": "Extremely long document content...",
  "maxLength": 500
}
```

## Expected Output
A JSON object containing the summarized text.
