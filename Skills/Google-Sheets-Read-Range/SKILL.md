---
name: Google Sheets Read Range
description: Atomic node skill to read a range from a Google Sheet using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the retrieval fails.

# Google Sheets Read Range

This skill allows the agent to read data from a specific range in a Google Sheet.

## Cognitive Directives
WHEN [Data needs to be retrieved from a Google Sheet range]
THEN [Execute the `gworkspace_sheets_read` plugin tool]

## Schema Example
```json
{
  "spreadsheetId": "sheet_id_123",
  "range": "Sheet1!A1:D10"
}
```

## Expected Output
A JSON object containing the values retrieved from the sheet.
