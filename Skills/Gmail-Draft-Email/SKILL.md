---
name: Gmail Draft Email
description: Atomic node skill to create a draft email using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the operation fails.

# Gmail Draft Email

This skill allows the agent to create a draft email.

## Cognitive Directives
WHEN [Requested to draft an email for later review or sending]
THEN [Execute the `gworkspace_gmail_draft` plugin tool]

## Schema Example
```json
{
  "to": "client@example.com",
  "subject": "Proposal Draft",
  "body": "Here is the draft for the upcoming proposal..."
}
```

## Expected Output
A JSON object confirming the draft was created (including draft ID).
