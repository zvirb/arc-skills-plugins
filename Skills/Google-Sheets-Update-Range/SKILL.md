---
name: Google Sheets Update Range
description: Atomic node skill to update a range in Google Sheets using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the update fails.

# Google Sheets Update Range

This skill allows the agent to update a specific range in a Google Sheet using the native CLI.

## Cognitive Directives
WHEN [A range of cells needs to be updated in a Google Sheet]
THEN [Execute the native terminal command `gog sheets update <spreadsheetId> <range> --values-json '[["..."]]'`]

## Schema Example
```json
{
  "command": "gog sheets update sheet_id_123 \"Tab1!A1:B1\" --values-json '[[\"Val1\", \"Val2\"]]' --json"
}
```

## Expected Output
A JSON object confirming the update.
