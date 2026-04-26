---
name: Gmail Search Emails
description: Atomic node skill to search for emails using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the search fails.

# Gmail Search Emails

This skill allows the agent to search for emails in Gmail using specific queries.

## Cognitive Directives
WHEN [Requested to search for an email or find specific communications]
THEN [Execute the `gworkspace_gmail_search` plugin tool]

## Schema Example
```json
{
  "query": "from:example@gmail.com subject:invoice"
}
```

## Expected Output
A JSON array containing email headers (id, threadId, snippet) or a "no results found" message.
