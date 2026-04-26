---
name: Google Drive Share File
description: Atomic node skill to share a file in Google Drive using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the operation fails.

# Google Drive Share File

This skill allows the agent to share a file with specific users or update permissions.

## Cognitive Directives
WHEN [A file ID is provided and sharing permissions need to be modified]
THEN [Execute the `gworkspace_drive_share` plugin tool]

## Schema Example
```json
{
  "fileId": "file_id_123",
  "emailAddress": "collaborator@example.com",
  "role": "writer",
  "type": "user"
}
```

## Expected Output
A JSON object confirming the sharing operation.
