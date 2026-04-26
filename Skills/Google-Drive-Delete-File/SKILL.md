---
name: Google Drive Delete File
description: Atomic node skill to delete a file from Google Drive using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the deletion fails.

# Google Drive Delete File

This skill allows the agent to delete a specific file from Google Drive.

## Cognitive Directives
WHEN [A file ID is provided and the file must be removed from Google Drive]
THEN [Execute the `gworkspace_drive_delete` plugin tool]

## Schema Example
```json
{
  "fileId": "file_id_123"
}
```

## Expected Output
A JSON object confirming the deletion.
