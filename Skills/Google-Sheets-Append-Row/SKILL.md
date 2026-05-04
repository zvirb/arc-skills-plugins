---
name: google-sheets-append-row
description: "Atomic node to append data to a Google Sheet with strict validation."
allowed-tools: [exec]
---

# Google Sheets Append Row

This skill directs the agent to append a single row of data to a specified spreadsheet.

## Execution Directives
1. **Prepare Command:** Construct the `gog` command using the following schema:
   - `gog sheets append <SPREADSHEET_ID> --range "<SHEET_NAME>!A:A" --values '[["col1", "col2"]]'`
2. **Execute Script:** Wrap the command in the hardened script.
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-sheets-append-row/scripts/run.sh sheets append <ID> --range "<RANGE>" --values '<JSON_ARRAY>'`
3. **Verify Jidoka:** Ensure the output confirms the range updated.
4. **Handle Failure:** If status is ERROR, capture the message and retry.

## Input Schema (JSON)
```json
{
  "spreadsheetId": "string",
  "range": "Sheet1!A:Z",
  "values": [["row1_val1", "row1_val2"]]
}
```
