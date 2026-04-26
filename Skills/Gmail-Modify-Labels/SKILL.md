---
name: Gmail Modify Labels
description: Atomic node skill to add or remove labels from an email using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the operation fails.

# Gmail Modify Labels

This skill allows the agent to batch modify labels on a specific email.

## Cognitive Directives
WHEN [An email ID is provided and labels need to be added or removed]
THEN [Execute the `gworkspace_gmail_modify_labels` plugin tool]

## Schema Example
```json
{
  "id": "12345abcde67890",
  "addLabels": ["IMPORTANT", "WORK"],
  "removeLabels": ["UNREAD"]
}
```

## Expected Output
A JSON object confirming the label modifications.
