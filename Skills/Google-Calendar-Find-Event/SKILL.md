---
name: google-calendar-find-event
description: "Hardened script-based execution for google-calendar-find-event."
allowed-tools: [exec]
---

# Google Calendar Find Event

This skill directs the agent to retrieve events from a Google Calendar using the `gog` CLI directly.

## Execution Directives
1. **Execute Command**: Run the `gog` command directly with target parameters.
   - Command: `gog calendar list <calendarId> [--from <date>] [--to <date>] [--query "<search>"] --json --results-only`
2. **Verify Output**: Ensure the response is a JSON array of events.
3. **Handle Failure**: If no events are found or the API fails, report the raw `gog` output.

## Input Schema (JSON)
```json
{
  "calendarId": "primary",
  "from": "today",
  "to": "tomorrow",
  "query": "optional search"
}
```
