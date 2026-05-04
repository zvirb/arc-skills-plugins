---
name: google-calendar-create-event
description: "Atomic node to create a Google Calendar event with strict validation."
allowed-tools: [exec]
---

# Google Calendar Create Event

This skill directs the agent to schedule a new event on the primary calendar using the `gog` CLI.

## Execution Directives
1. **Prepare Command:** Construct the `gog` command using the following schema:
   - `gog calendar create primary --summary "<Title>" --from "<ISO_START>" --to "<ISO_END>"`
2. **Execute Script:** Wrap the command in the hardened script to capture errors.
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-calendar-create-event/scripts/run.sh calendar create primary --summary "..." --from "..." --to "..."`
3. **Verify Jidoka:** Inspect the output. A successful result MUST return a JSON object containing the `id` of the new event.
4. **Handle Failure:** If the script returns `{"STATUS": "ERROR"}`, analyze the `ERROR_MSG` and retry with corrected parameters (Max 3 retries).

## Input Schema (JSON)
```json
{
  "summary": "Meeting Title",
  "from": "2026-05-04T10:00:00Z",
  "to": "2026-05-04T11:00:00Z"
}
```
