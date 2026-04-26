---
name: Google Docs Create Document
description: Atomic node skill to create a Google Doc using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if document creation fails.

# Google Docs Create Document

This skill allows the agent to create a new Google Document.

## Cognitive Directives
WHEN [A new Google Doc needs to be created]
THEN [Execute the `gworkspace_docs_create` plugin tool]

## Schema Example
```json
{
  "title": "Meeting Notes"
}
```

## Expected Output
A JSON object confirming the document was created (including documentId).
