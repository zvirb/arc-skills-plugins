---
name: google-calendar-create-event
description: "Directives for creating new Google Calendar events. Uses high-fidelity ISO strings and deterministic flags."
allowed-tools: [workspace_gog]
triggers: [create event, schedule meeting, book time, new calendar entry]
negative-triggers: [find event, list calendar, delete event, update event]
---

# Google Calendar Create Event Directive

Use the `workspace_gog` tool to create a new event.

## Execution Directives
1. **Time Management:**
   - Use ISO 8601 format: `YYYY-MM-DDTHH:MM:SS+10:00` (Enforce `+10:00` for Melbourne/Sydney).
2. **Execute Create:**
   - **Syntax:** `calendar create primary --summary "<summary>" --from "<start>" --to "<end>" --json`
   - **Optional:** Use `--description "<text>"` or `--location "<text>"` if provided.
3. **Verify:** Confirm the `id` of the newly created event.

---
name: google-calendar-delete-event
description: "Directives for removing Google Calendar events. Requires force flag to prevent hanging."
allowed-tools: [workspace_gog]
triggers: [delete event, cancel meeting, remove from calendar]
---

# Google Calendar Delete Event Directive

Use the `workspace_gog` tool to remove an event.

## Execution Directives
1. **ID Retrieval:** If `eventId` is unknown, use `calendar list` or `calendar find` first.
2. **Execute Delete:**
   - **Syntax:** `calendar delete primary <eventId> --force --json`
   - **Critical:** You MUST include `--force` to bypass interactive confirmation.

---
name: google-calendar-find-event
description: "Directives for searching or listing calendar events."
allowed-tools: [workspace_gog]
triggers: [find event, list schedule, what is my day like, calendar search]
---

# Google Calendar Find Event Directive

Use the `workspace_gog` tool to search events.

## Execution Directives
1. **Execute Search:**
   - **List Syntax:** `calendar list --json`
   - **Filtered Search:** `calendar list --json | jq ...` (The agent should perform filtering on the returned JSON).

---
name: google-calendar-update-event
description: "Directives for modifying existing calendar events."
allowed-tools: [workspace_gog]
triggers: [update event, reschedule, change summary]
---

# Google Calendar Update Event Directive

Use the `workspace_gog` tool to modify an event.

## Execution Directives
1. **Execute Update:**
   - **Syntax:** `calendar update primary <eventId> [flags] --json`
   - **Available Flags:**
     - `--summary "<text>"`
     - `--from "<ISO>"`
     - `--to "<ISO>"`
     - `--description "<text>"`
     - `--force` (Always include to skip confirmation)
