---
name: Google Sheets Append Row
description: Atomic node skill to append a row to a Google Sheet using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the operation fails.

# Google Sheets Append Row

This skill allows the agent to append a new row of data to a specific spreadsheet and range.

## Cognitive Directives
WHEN [New data needs to be logged or added to a Google Sheet]
THEN [Execute the `gworkspace_sheets_append` plugin tool]

## Schema Example
```json
{
  "spreadsheetId": "sheet_id_123",
  "range": "Sheet1!A1",
  "values": [["Column1", "Column2", "Value"]]
}
```

## Expected Output
A JSON object confirming the row was appended.
