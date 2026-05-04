---
name: llm-summarize-text
description: Atomic node to generate concise summaries of text.
---

# LLM Summarize Text

This skill directs the agent to condense long text into a brief, high-impact summary.

## Execution Directives
1. **Determine Parameters:** Set the `maxLength` (default: 500 characters) and context for the summary.
2. **Execute Summarization:** Run the `llm_summarize_text` tool.
3. **Verify Quality:** If the summary is truncated or fails to capture key points, re-prompt with specific refinement instructions.
4. **Report Summary:** Provide the final summarized text to the user.

## Expected Output
A JSON object containing the summarized text.
