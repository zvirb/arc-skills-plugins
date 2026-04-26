---
name: Google Calendar Update Event
description: Atomic node skill to update an existing calendar event using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the operation fails.

# Google Calendar Update Event

This skill allows the agent to update details of an existing Google Calendar event.

## Cognitive Directives
WHEN [An event ID is provided and details need to be modified]
THEN [Execute the `gworkspace_calendar_update` plugin tool]

## Schema Example
```json
{
  "id": "event_id_123",
  "summary": "Updated Meeting Title",
  "start": { "dateTime": "2026-04-26T14:00:00Z" }
}
```

## Expected Output
A JSON object confirming the update.
