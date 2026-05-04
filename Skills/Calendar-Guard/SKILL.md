---
name: calendar-guard
description: Atomic node skill to defend the schedule by injecting recovery blocks.
os: all
requires:
  bins: [gog]
---

# Calendar Guard

This skill evaluates schedule density and automatically injects recovery blocks into Google Calendar.

## Execution Directives
1. **Fetch Commitments:** Execute `gog calendar events primary --from "today" --to "tomorrow" --json` to retrieve the next 24 hours of events.
2. **Analyze Load:** Execute `llm_identify_conflicts` to identify periods of high cognitive load within the retrieved events.
3. **Request Approval:** If high-load periods are detected, present the proposed "Recovery Block" times to the user. Wait for explicit "Approve" or "Yes" confirmation.
4. **Inject Blocks:** After receiving approval, execute `gog calendar create primary --summary "Recovery Block" --from "<start>" --to "<end>"` for each approved block.
5. **Verify Injection:** Parse the JSON confirmation for each created event. Log successes and report any failures to the user.

## Expected Output
A JSON log of any recovery blocks successfully injected.
