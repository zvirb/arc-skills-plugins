---
name: Event-Cancellation-Reconciler
description: Workflow-driven skill that autonomously detects cancelled events in emails and syncs the calendar state by deleting or updating orphaned calendar blocks.
os: all
requires:
  bins:
    - gog
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is broken down into atomic steps: parsing the email intent, locating the stale event, and reconciling the state.
- **Standardized Work (Hyojun Sagyo):** This node represents the standardized workflow for state-syncing Google Calendar based on Gmail cancellation notices.
- **Jidoka (自働化):** Includes autonomous self-healing loops. If no event is found during the search phase, the agent stops and gracefully reports completion.

# Event Cancellation Reconciler

This skill orchestrates multiple tools to automatically remove or update calendar events when an email indicates a cancellation or reschedule, preventing stale state and double-booking.

## Cognitive Directives
WHEN [Requested to handle a cancelled event from an email OR when reading an email indicating a cancellation/reschedule]
THEN [
  Execute the following Jidoka-validated loop:
  1. Extract Event Details: Use the `LLM-Extract-JSON` or `LLM-Extract-Action-Items` skill against the email body to extract the `original_date`, `original_time`, and `target_entity` (event subject).
     - **Verification Step (Jidoka):** Verify the dates and subject are extracted. IF extraction fails, ask the user for the event details and STOP.
  2. Locate Orphaned Event: Execute the native terminal command `gog calendar search "<target_entity>" --json` or `gog calendar events primary --from "<original_date>T00:00:00Z" --to "<original_date>T23:59:59Z" --json` to locate the event ID.
     - **Verification Step (Jidoka):** Check if any events are returned. IF no matching event is found, reply "No conflicting calendar events found to clean up" and STOP.
  3. Reconcile State: Execute `gog calendar delete <event_id>` to clear the block, or optionally `gog calendar update <event_id> --summary "[CANCELLED] <original_title>"` to preserve a record.
     - **Verification Step (Jidoka):** Verify the native CLI returns a success response. IF it fails, log the failure and attempt to retry once before prompting the user.
  4. Notify: Reply to the user stating the cancellation has been processed and the calendar block is cleared.
]

## Expected Output
A confirmation message stating the calendar has been synced and the specific event has been deleted or marked as cancelled.
