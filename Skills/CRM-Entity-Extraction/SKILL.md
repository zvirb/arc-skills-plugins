---
name: CRM Entity Extraction
description: Workflow-driven skill that bridges Gmail data extraction logic to Google Sheets or Google Contacts via Composio.
os: windows
requires:
  bins:
  env:
    - COMPOSIO_API_KEY
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# CRM Entity Extraction

This skill orchestrates a workflow to extract structured data (persons, organizations, dates) from raw text and append it to a CRM spreadsheet.

## Workflow Orchestration
This skill is an autonomous workflow. You MUST chain the following atomic actions using your native tools provided by the LLMTransformations and GoogleWorkspace plugins:
1. **LLM-Extract-JSON**: Extracts structured entities from unstructured text.
2. **Google-Sheets-Append-Row**: Appends the extracted data to a specified Google Sheet.

## Role
You are a data entry agent. You should process all business-related emails or notes through this workflow to keep the CRM updated.

## Input
A string of text (e.g., an email body) containing potential CRM data.

## Expected Output
A JSON summary of the extracted data and the append result.
