---
name: crm-entity-extraction
description: Extracts entities from Gmail and bridges to Google Sheets or Google Contacts via Composio.
version: 1.1.0
os:
  - windows
  - linux
  - darwin
requires:
  bins:
    - python
    - lobster
  env:
    - COMPOSIO_API_KEY
metadata:
  orchestrator: OpenProse
  security: Lobster
  type: pipeline
---

# CRM Entity Extraction (OpenProse Pipeline)

This skill utilizes an OpenProse pipeline and localized Python scripts to extract Named Entities from inbound emails and push them directly into a designated Google Sheet (acting as a lightweight CRM database) or directly into Google Contacts with custom labels via the Composio Google Workspace integrations. To maintain zero-trust security and auditability, all execution boundaries are enforced via `lobster`.

## Directives
- **Input:** Raw inbound email text.
- **Process:** Extract entities using the local `extractor.py` Python script and write directly to Google Sheets or Google Contacts via Composio.
- **Output:** Structured JSON output mapping the entities.

## Execution Rules
1. **Boundary Enforcement:** Any shell execution required for Regex/NER processing MUST be wrapped in the `lobster` sandbox. 
   - *Security Rule:* Do NOT concatenate raw input strings into shell commands. Pass input via secure argument passing or environment variables.
   - Example: `lobster exec --env INPUT_TEXT="$GMAIL_TEXT" python Skills/CRM-Entity-Extraction/extractor.py "$INPUT_TEXT"`
2. **OpenProse Orchestration:** Treat each extraction step as a deterministic state. If NER extraction confidence is low, halt the pipeline and do not execute the Composio API call.
