---
name: Google Sheets Create Spreadsheet
description: Atomic node skill to create a new Google Spreadsheet using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the operation fails.

# Google Sheets Create Spreadsheet

This skill allows the agent to create a new Google Spreadsheet.

## Cognitive Directives
WHEN [A new spreadsheet needs to be created in Google Drive]
THEN [Execute the `gworkspace_sheets_create` plugin tool]

## Schema Example
```json
{
  "title": "New Project Budget"
}
```

## Expected Output
A JSON object confirming the spreadsheet was created (including spreadsheetId and URL).
