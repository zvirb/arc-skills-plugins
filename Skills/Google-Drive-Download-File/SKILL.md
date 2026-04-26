---
name: Google Drive Download File
description: Atomic node skill to download a file from Google Drive using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the download fails.

# Google Drive Download File

This skill allows the agent to download the content of a file from Google Drive.

## Cognitive Directives
WHEN [A file ID is provided and the local content is required]
THEN [Execute the `gworkspace_drive_download` plugin tool]

## Schema Example
```json
{
  "fileId": "file_id_123"
}
```

## Expected Output
A JSON object containing the file content (or a path/link to the downloaded file).
