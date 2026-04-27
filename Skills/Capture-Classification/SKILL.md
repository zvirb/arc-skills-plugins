---
name: capture-classification
description: Workflow-driven skill that routes unstructured audio transcripts or quick notes to Google Tasks or LanceDB based on urgency.
os: all
requires:
  bins: [gog]
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
  Execute the following Jidoka-validated loop:
  1. Execute `llm_classify_intent` (Sub-Agent) with categories: ["Actionable", "Informational"].
     - **Verification Step (Jidoka):** Verify the sub-agent returns exactly one of the requested categories. IF it returns an invalid or hallucinated category, instruct it to correct the output and retry.
  2. IF "Actionable", Execute the native terminal command `gog tasks add @default --title "..."` with the summary.
     - **Verification Step (Jidoka):** Check if the native command returns a successful JSON response. IF it fails, wait 3 seconds, and retry. IF it still fails after 3 attempts, report the error and STOP.
  3. IF "Informational", Execute `vector_store_upsert` to save it as reference material.
     - **Verification Step (Jidoka):** Verify the vector store confirms a successful upsert. IF it fails, report the error and STOP.
]

## Expected Output
A JSON log confirming the routed destination and action taken.
