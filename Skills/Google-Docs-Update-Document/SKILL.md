---
name: Google Docs Update Document
description: Atomic node skill to update a Google Doc using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the update fails.

# Google Docs Update Document

This skill allows the agent to update or append content to a Google Document.

## Cognitive Directives
WHEN [A document ID is provided and content needs to be updated or appended]
THEN [Execute the `gworkspace_docs_update` plugin tool]

## Schema Example
```json
{
  "documentId": "document_id_123",
  "text": "Adding new project details...",
  "index": 1
}
```

## Expected Output
A JSON object confirming the update.
