---
name: Gmail Send Email
description: Atomic node skill to send an email using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the operation fails.

# Gmail Send Email

This skill allows the agent to send a new email.

## Cognitive Directives
WHEN [Requested to send a new email message]
THEN [Execute the `gworkspace_gmail_send` plugin tool]

## Schema Example
```json
{
  "to": "recipient@example.com",
  "subject": "Project Update",
  "body": "The task has been completed successfully."
}
```

## Expected Output
A JSON object confirming the email was sent (including message ID).
