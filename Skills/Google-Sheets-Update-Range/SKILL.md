---
name: Google Sheets Update Range
description: Atomic node skill to update a range in a Google Sheet using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the operation fails.

# Google Sheets Update Range

This skill allows the agent to update data in a specific range of a Google Sheet.

## Cognitive Directives
WHEN [Existing data needs to be modified or updated in a Google Sheet range]
THEN [Execute the `gworkspace_sheets_update` plugin tool]

## Schema Example
```json
{
  "spreadsheetId": "sheet_id_123",
  "range": "Sheet1!A1",
  "values": [["New Header 1", "New Header 2"]]
}
```

## Expected Output
A JSON object confirming the range was updated.
