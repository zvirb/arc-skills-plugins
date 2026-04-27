---
name: executive-assistant-time-blocking
description: Workflow-driven skill that autonomously acts as an executive assistant to block out calendar time for incomplete tasks based on urgency and estimated duration.
os: all
requires:
  bins: [gog]
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill orchestrates multiple atomic nodes (tasks retrieval, cognitive assessment, calendar retrieval, gap analysis, and event creation) into a cohesive workflow, ensuring each step is validated before proceeding.
- **Standardized Work (Hyojun Sagyo):** This node represents the standardized standard operating procedure (SOP) for automated time-blocking and scheduling of user tasks.
- **Jidoka (自働化):** This workflow includes autonomous defect detection. It will check for calendar overlaps, verify event creation, and repeat scheduling steps if a slot is double-booked or an event fails to create.

# Executive Assistant Time Blocking

This skill directs the agent to evaluate current incomplete tasks from Google Tasks, estimate their duration and urgency, and sequentially schedule them into available gaps in Google Calendar.

## Cognitive Directives

WHEN [Requested to schedule tasks, time-block the backlog, or act as an executive assistant for schedule management]
THEN [
  Execute the following Jidoka-validated loop:

  1. **Task Collection:** Execute the native terminal command `gog tasks list @default --json` to retrieve all current incomplete tasks.
     - **Verification Step (Jidoka):** Check if the returned output is a valid JSON array of tasks. IF it fails or errors, report the error and STOP. IF empty, report that there are no tasks to schedule and STOP.

  2. **Cognitive Assessment (Triage):**
     - For each task, autonomously estimate the time required to complete it.
     - Assess the urgency of each task.
     - Judge when the task should be scheduled (e.g., today vs. another day soon).
     - **Verification Step (Jidoka):** Verify that *every* collected task has been assigned an estimated duration, an urgency score, and a target date. IF any task is missing these values, correct the assessment and retry before proceeding.

  3. **Schedule Retrieval:** 
     - For the target days identified, execute `gog calendar events primary --from "<start_date_iso>" --to "<end_date_iso>" --json` to retrieve currently booked events.
     - **Verification Step (Jidoka):** Verify the command returns a valid JSON array of events. IF it returns an error (e.g., rate limit or network error), wait 3 seconds and retry (max 3 times). IF it still fails, report the error and STOP.

  4. **Gap Analysis:**
     - Analyze the retrieved calendar events to identify gaps in the schedule.
     - **Constraint Check:** Ensure that gaps respect standard human needs (e.g., leave appropriate blocks of time for eating meals and sleeping).
     - **Verification Step (Jidoka):** Verify that the calculated gaps for a target day are large enough to fit the assigned tasks. IF there is insufficient time on the target day, reassign the overflow tasks to the next day, and repeat Step 3 (Schedule Retrieval) for the new target day.

  5. **Sequential Time Blocking (Jidoka Loop):**
     - Sequentially fit tasks into the schedule gaps based on their estimated duration and urgency.
     - For each fitted task, execute `gog calendar create primary --summary "[Task] <Task Title>" --from "<start_time_iso>" --to "<end_time_iso>" --json`.
     - **Verification Step:** After creation, execute `gog calendar events primary --from "<start_time_iso>" --to "<end_time_iso>" --json` again for that time slot to verify the event was correctly created and recalculate remaining gaps.

  6. **Overlap Audit & Remediation:**
     - Once all tasks have been assigned a block, perform a final audit using `gog calendar events` across all modified days.
     - Double-check that there are no overlaps or double-booked slots.
     - IF double-booking is detected: Delete or reschedule the conflicting task event (`gog calendar delete primary <eventId>`) and repeat the scheduling steps (Steps 3-5) until all tasks are booked without conflict.
]

## Expected Output
A comprehensive JSON or Markdown summary of the scheduled tasks, detailing the timeline, any constraints respected, and confirmation of overlap-free scheduling.
