---
name: Google Docs Append Text
description: Atomic node skill to exclusively append text to a Google Document.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, strictly limited to appending text to a document, preventing schema hallucination and ensuring single-responsibility.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the operation fails.

# Google Docs Append Text

This skill allows the agent to append text to the end of an existing Google Document using the native CLI. It does NOT do find and replace.

## Cognitive Directives
WHEN [Text needs to be added or appended to the end of a Google Doc]
THEN [Execute the native terminal command `gog docs write <docId> --text "..."`]

## Schema Example
```json
{
  "command": "gog docs write doc_id_123 --text \"This is the new text to append.\""
}
```

## Jidoka Validation Loop
1. Try: Execute the command.
2. Evaluate: Check the response to confirm the text was appended successfully.
3. Correct/Fail: If it failed or hallucinated parameters, retry up to 3 times (max_retries=3) with the exact error.
4. Proceed: Return the final confirmation.

## Expected Output
A JSON object or confirmation string indicating the text was appended successfully.
