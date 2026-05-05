---
name: google-calendar-create-event
description: "Atomic node to create a Google Calendar event with strict validation."
allowed-tools: [exec]
---

# Google Calendar Create Event

This skill directs the agent to schedule a new event on the primary calendar using the `gog` CLI directly.

## Execution Directives
1. **Execute Command**: Run the `gog` command directly.
   - Command: `gog calendar create primary --summary "<Title>" --from "<ISO_START>" --to "<ISO_END>" --json`
2. **Verify Output**: Ensure the response is a JSON object containing the new event `id`.
3. **Handle Failure**: If the command fails, report the error output from `gog`.

## Input Schema (JSON)
```json
{
  "summary": "Meeting Title",
  "from": "2026-05-04T10:00:00Z",
  "to": "2026-05-04T11:00:00Z"
}
```
