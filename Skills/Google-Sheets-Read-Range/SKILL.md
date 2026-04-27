---
name: Google Sheets Read Range
description: Atomic node skill to read a range from Google Sheets using the gog CLI.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the CLI's self-healing loop and will report errors if the read fails.

# Google Sheets Read Range

This skill allows the agent to read values from a specific range in a Google Sheet using the native CLI.

## Cognitive Directives
WHEN [Values from a range of cells need to be read from a Google Sheet]
THEN [Execute the native terminal command `gog sheets get <spreadsheetId> <range> --json`]

## Schema Example
```json
{
  "command": "gog sheets get sheet_id_123 \"Tab1!A1:D10\" --json"
}
```

## Expected Output
A JSON array containing the cell values.
