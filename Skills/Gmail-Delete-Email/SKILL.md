---
name: Gmail Delete Email
description: Atomic node skill to delete an email using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the deletion fails.

# Gmail Delete Email

This skill allows the agent to delete a specific email message.

## Cognitive Directives
WHEN [An email ID is provided and the message must be deleted or moved to trash]
THEN [Execute the `gworkspace_gmail_delete` plugin tool]

## Schema Example
```json
{
  "id": "12345abcde67890"
}
```

## Expected Output
A JSON object confirming the deletion.
