---
name: Google Calendar Find Event
description: Atomic node skill to search for events in Google Calendar using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the search fails.

# Google Calendar Find Event

This skill allows the agent to search for events in Google Calendar within a specific time range.

## Cognitive Directives
WHEN [Requested to find events or check schedule for a specific period]
THEN [Execute the `gworkspace_calendar_find` plugin tool]

## Schema Example
```json
{
  "query": "Sync Meeting",
  "timeMin": "2026-04-26T00:00:00Z",
  "timeMax": "2026-04-26T23:59:59Z"
}
```

## Expected Output
A JSON array of event objects matching the criteria.
