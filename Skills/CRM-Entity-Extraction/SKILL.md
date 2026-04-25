---
name: crm-entity-extraction
description: Extracts entities from Gmail and bridges to a local SQLite CRM via OpenProse pipeline.
version: 1.0.0
os:
  - windows
  - linux
  - darwin
requires:
  bins:
    - python
    - lobster
    - datasette
metadata:
  orchestrator: OpenProse
  security: Lobster
  type: pipeline
---

# CRM Entity Extraction (OpenProse Pipeline)

This skill utilizes an OpenProse pipeline and localized Python scripts to extract Named Entities from Gmail data and push them directly to a local, lightweight SQLite CRM (`Memory/crm.db`). This database can then be served and interacted with using the open-source `Datasette` application. To maintain zero-trust security and auditability, all execution boundaries are enforced via `lobster`.

## Directives
- **Input:** Raw Gmail thread text.
- **Process:** Extract entities using the local `extractor.py` Python script and write directly to `crm.db`.
- **Output:** Structured record insertion confirming the SQLite update.

## Execution Rules
1. **Boundary Enforcement:** Any shell execution required for Regex/NER processing MUST be wrapped in the `lobster` sandbox. 
   - *Security Rule:* Do NOT concatenate raw input strings into shell commands. Pass input via secure argument passing or environment variables.
   - Example: `lobster exec --env INPUT_TEXT="$GMAIL_TEXT" python Skills/CRM-Entity-Extraction/extractor.py "$INPUT_TEXT"`
2. **OpenProse Orchestration:** Treat each extraction step as a deterministic state. If NER extraction confidence is low, halt the pipeline and do not insert into SQLite.

## Data Viewing (Datasette)
The `extractor.py` script autonomously scaffolds and manages the SQLite database upon its first run. No database installation is required.
To view and interact with the extracted CRM data via a lightweight web interface:
1. Ensure Datasette is installed on the host: `pip install datasette`
2. Launch the viewer: `datasette Memory/crm.db`
