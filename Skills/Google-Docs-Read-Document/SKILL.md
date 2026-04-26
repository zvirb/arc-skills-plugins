---
name: Google Docs Read Document
description: Atomic node skill to read a Google Doc using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific path before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if reading fails.

# Google Docs Read Document

This skill allows the agent to read the content of a Google Document.

## Cognitive Directives
WHEN [A document ID is provided and the content needs to be retrieved]
THEN [Execute the `gworkspace_docs_read` plugin tool]

## Schema Example
```json
{
  "documentId": "document_id_123"
}
```

## Expected Output
A JSON object containing the document's content and metadata.
