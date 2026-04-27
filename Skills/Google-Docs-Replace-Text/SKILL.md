---
name: Google Docs Replace Text
description: Atomic node skill to exclusively find and replace text in a Google Document.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, strictly limited to replacing text in a document, preventing schema hallucination and ensuring single-responsibility.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the operation fails.

# Google Docs Replace Text

This skill allows the agent to find and replace text in an existing Google Document using the native CLI. It does NOT append new text.

## Cognitive Directives
WHEN [Specific text needs to be found and replaced in a Google Doc]
THEN [Execute the native terminal command `gog docs edit <docId> "<find_text>" "<replace_text>"`]

## Schema Example
```json
{
  "command": "gog docs edit doc_id_123 \"old text\" \"new text\""
}
```

## Jidoka Validation Loop
1. Try: Execute the command.
2. Evaluate: Check the response to confirm the text was replaced successfully.
3. Correct/Fail: If it failed or hallucinated parameters, retry up to 3 times (max_retries=3) with the exact error.
4. Proceed: Return the final confirmation.

## Expected Output
A JSON object or confirmation string indicating the replacement was successful.
