---
name: Google Drive Upload File
description: Atomic node skill to upload a file to Google Drive using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the upload fails.

# Google Drive Upload File

This skill allows the agent to upload a file to Google Drive.

## Cognitive Directives
WHEN [Requested to upload a local file or data to Google Drive]
THEN [Execute the `gworkspace_drive_upload` plugin tool]

## Schema Example
```json
{
  "name": "Report.pdf",
  "content": "[BASE64_OR_PATH]",
  "mimeType": "application/pdf"
}
```

## Expected Output
A JSON object confirming the upload (including file ID).
