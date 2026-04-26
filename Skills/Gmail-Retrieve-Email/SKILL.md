---
name: Gmail Retrieve Email
description: Atomic node skill to retrieve specific email content using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the retrieval fails.

# Gmail Retrieve Email

This skill retrieves the full content of a specific email message given its unique ID.

## Cognitive Directives
WHEN [An email ID is provided and full content retrieval is required]
THEN [Execute the `gworkspace_gmail_retrieve` plugin tool]

## Schema Example
```json
{
  "id": "12345abcde67890"
}
```

## Expected Output
A JSON object containing the email details (subject, from, to, body, labels, date).
