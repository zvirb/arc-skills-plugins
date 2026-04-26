---
name: capture-classification
description: Workflow-driven skill that routes unstructured audio transcripts or quick notes to Google Tasks or LanceDB based on urgency.
os: windows
requires:
  bins:
  env:
    - COMPOSIO_API_KEY
    - LANCE_DB_PATH
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# Capture Classification

This skill orchestrates a workflow to act as a semantic router for inbound text. It evaluates intent and urgency before routing to the appropriate destination.

## Workflow Orchestration
This skill is an autonomous workflow. You MUST chain the following atomic actions using your native tools provided by the LLMTransformations and GoogleWorkspace plugins:
1. **LLM-Classify-Intent**: Evaluates the text against urgency heuristics and intent (Actionable vs Informational).
2. **Google-Tasks-Create-Task**: Used if the item is actionable.
3. **Vector-Store-Upsert-Memory**: Used if the item is informational/reference material.

## Role
You are a semantic router. You should process all inbound captures through this workflow to ensure they are stored or acted upon correctly.

## Input
Unstructured audio transcript or note text.

## Expected Output
A JSON log confirming the routed destination and action taken.
