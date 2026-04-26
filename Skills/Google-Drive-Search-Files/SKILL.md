---
name: Google Drive Search Files
description: Atomic node skill to search for files in Google Drive using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the search fails.

# Google Drive Search Files

This skill allows the agent to search for files in Google Drive using specific queries or filenames.

## Cognitive Directives
WHEN [Requested to find a file in Google Drive or search for specific content]
THEN [Execute the `gworkspace_drive_search` plugin tool]

## Schema Example
```json
{
  "q": "name contains 'Project' and mimeType = 'application/pdf'"
}
```

## Expected Output
A JSON array of file objects (id, name, mimeType) matching the query.
