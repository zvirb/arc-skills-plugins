---
name: Google Calendar Delete Event
description: Atomic node skill to delete a calendar event using the GoogleWorkspace plugin.
os: all
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the deletion fails.

# Google Calendar Delete Event

This skill allows the agent to delete a specific event from Google Calendar.

## Cognitive Directives
WHEN [An event ID is provided and the event must be removed from the calendar]
THEN [Execute the `gworkspace_calendar_delete` plugin tool]

## Schema Example
```json
{
  "id": "event_id_123"
}
```

## Expected Output
A JSON object confirming the deletion.
