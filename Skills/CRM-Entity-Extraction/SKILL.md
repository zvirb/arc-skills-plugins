---
name: CRM Entity Extraction
description: Workflow-driven skill that bridges Gmail data extraction logic to Google Sheets or Google Contacts via Composio.
os: windows
requires:
  bins: []
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
  1. Execute `llm_extract_json` (Sub-Agent) to extract structured entities (name, org, date).
  2. Execute `gworkspace_sheets_append` to add the extracted JSON row to the CRM spreadsheet.
]

## Expected Output
A JSON summary of the extracted data and the append result.
