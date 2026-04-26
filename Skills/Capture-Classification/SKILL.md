---
name: capture-classification
description: Workflow-driven skill that routes unstructured audio transcripts or quick notes to Google Tasks or LanceDB based on urgency.
os: windows
requires:
  bins: []
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.

# Capture Classification

This skill acts as a semantic router for inbound text, evaluating intent and urgency before routing to the appropriate destination.

## Cognitive Directives
WHEN [Unstructured audio transcript or note text is captured]
THEN [
  1. Execute `llm_classify_intent` (Sub-Agent) with categories: ["Actionable", "Informational"].
  2. IF "Actionable", Execute `gworkspace_tasks_create` with the summary.
  3. IF "Informational", Execute `vector_store_upsert` to save it as reference material.
]

## Expected Output
A JSON log confirming the routed destination and action taken.
