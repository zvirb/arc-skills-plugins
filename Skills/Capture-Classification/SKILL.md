---
name: kebab-case-auto-fix
description: Semantic router for unstructured audio transcripts or notes.
os: all
requires:
  bins: [gog]
---

# Capture Classification

This skill routes inbound text to Google Tasks or reference memory based on intent.

## Execution Directives
1. **Classify Intent:** Execute `llm_classify_intent` on the input text with categories: `["Actionable", "Informational"]`.
2. **Verify Category:** Ensure the model returns exactly one valid category. If invalid, re-prompt the model to select from the allowed list.
3. **Route Actionable Items:** If classified as "Actionable", execute `gog tasks add @default --title "<summary>"` using the extracted task description.
4. **Route Informational Items:** If classified as "Informational", execute `vector_store_upsert` to save the content into persistent reference memory.
5. **Report Outcome:** Notify the user of the final destination (Tasks or Vector Store) and provide the relevant ID or confirmation status.

## Expected Output
A JSON log confirming the routed destination and action taken.
