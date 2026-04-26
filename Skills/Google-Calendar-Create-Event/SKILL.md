---
name: Google Calendar Create Event
description: Atomic node skill to create a new calendar event using the GoogleWorkspace plugin.
os: windows
requires:
  plugins:
    - google-workspace-plugin
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It relies on the plugin's self-healing loop and will report errors if the creation fails.

# Google Calendar Create Event

This skill allows the agent to create a new event in Google Calendar.

## Cognitive Directives
WHEN [A new event needs to be scheduled or added to the calendar]
THEN [Execute the `gworkspace_calendar_create` plugin tool]

## Schema Example
```json
{
  "summary": "Meeting with Client",
  "location": "Virtual",
  "start": { "dateTime": "2026-04-26T10:00:00Z" },
  "end": { "dateTime": "2026-04-26T11:00:00Z" }
}
```

## Expected Output
A JSON object confirming the event was created (including event ID).
