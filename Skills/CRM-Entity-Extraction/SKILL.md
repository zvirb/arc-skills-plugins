---
name: crm-entity-extraction
description: Atomic node skill to extract CRM data from text and append to Google Sheets.
os: all
requires:
  bins: [gog]
---

# CRM Entity Extraction

This skill directs the agent to extract structured business entities and log them to a central CRM spreadsheet.

## Execution Directives
1. **Extract Data:** Execute `llm_extract_json` on the source text using a schema for `name`, `organization`, and `contact_date`.
2. **Verify Extraction:** Inspect the resulting JSON. If empty or malformed, re-attempt extraction with a more specific prompt.
3. **Append to CRM:** Execute `gog sheets append <spreadsheetId> "Sheet1!A1" --values-json '[["$name", "$org", "$date"]]'` to commit the data.
4. **Confirm Commit:** Report the successful row insertion and the extracted values to the user.

## Expected Output
A JSON object confirming the extracted entities and the spreadsheet append status.
