---
name: executive-assistant-time-blocking
description: High-level orchestration skill to block out time for tasks.
os: all
requires:
  bins: [gog]
---

# Executive Assistant Time Blocking

This skill directs the agent to proactively schedule incomplete tasks into the user's calendar.

## Execution Directives
1. **Collect Backlog:** Execute `gog tasks list @default --json` to retrieve incomplete tasks.
2. **Triage & Estimate:** For each task, assign an estimated duration and urgency score.
3. **Fetch Schedule:** Execute `gog calendar events primary --from "today" --to "today + 3 days" --json` to identify current commitments.
4. **Identify Gaps:** Analyze the calendar to find available time blocks, respecting meal and sleep buffers.
5. **Propose Blocks:** Present a proposed time-blocking schedule to the user via the active message channel.
6. **Request Approval:** Wait for explicit human approval before modifying the calendar.
7. **Execute Blocking:** After approval, execute `gog calendar create` for each block and verify successful creation.

## Expected Output
A summary of the newly created calendar blocks and any tasks still pending.
