---
name: CRM Entity Extraction
description: Workflow-driven skill that bridges Gmail data extraction logic to Google Sheets or Google Contacts via Composio.
os: all
requires:
  bins: [gog]
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.

# CRM Entity Extraction

This skill extracts structured data (persons, organizations, dates) from raw text and appends it to a CRM spreadsheet.

## Cognitive Directives
WHEN [A business-related email or note containing CRM data is received]
THEN [
  Execute the following Jidoka-validated loop:
  1. Execute `llm_extract_json` (Sub-Agent) to extract structured entities (name, org, date).
     - **Verification Step (Jidoka):** Check if the sub-agent returns a valid JSON object matching the requested entity schema. IF it returns unstructured text or invalid JSON, instruct the sub-agent to format correctly and retry.
  2. Execute the native terminal command `gog sheets append <spreadsheetId> <range> --values-json '[["..."]]'` to add the extracted JSON row to the CRM spreadsheet.
     - **Verification Step (Jidoka):** Verify the `gog sheets append` command returns a successful JSON confirmation. IF the API request fails, wait 3 seconds and retry (max 3 times). IF it still fails, report the error and STOP.
]

## Expected Output
A JSON summary of the extracted data and the append result.
