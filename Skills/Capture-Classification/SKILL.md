---
name: capture-classification
description: Route unstructured audio transcripts or quick notes to Google Tasks or LanceDB based on urgency.
version: 1.0.0
os:
  - windows
  - linux
  - darwin
requires:
  bins:
    - python
  env:
    - COMPOSIO_API_KEY
    - LANCE_DB_PATH
metadata:
  orchestrator: OpenProse
  security: None
  type: pipeline
---

# Capture Classification

This skill acts as a semantic router. It evaluates inbound text against urgency heuristics.
If the engine determines the capture is an actionable item ("call the supplier today"), it pushes it directly to the default Google Tasks list via Composio.
If it is a conceptual design thought or reference material, it routes it to the local memory-lancedb instance to be embedded into the open-source vector database for future recall.

## Directives
- **Input:** Unstructured audio transcript or note text.
- **Process:** Classify intent and urgency using LLM prompt. Route to Google Tasks (Composio) or local LanceDB.
- **Output:** JSON confirming the routed destination and action taken.
