---
name: calendar-guard
description: Workflow-driven skill that autonomously defends your schedule to manage cognitive load and prevent burnout.
os: all
requires:
  bins: [gog]
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.

# Calendar Guard

This skill evaluates schedule density and automatically injects recovery blocks into your Google Calendar when needed to prevent burnout.

## Cognitive Directives
WHEN [Requested to check calendar for burnout risks OR running on a daily schedule]
THEN [
  Execute the following Jidoka-validated loop:
  1. Execute the native terminal command `gog calendar events primary --from "..." --to "..." --json` to retrieve events for the next 24 hours.
     - **Verification Step (Jidoka):** Check if the output is a valid JSON array. IF it fails or returns an error, wait 3 seconds, and retry. IF it still fails, report the error and STOP.
  2. Execute `llm_identify_conflicts` (Sub-Agent) to analyze the event list for periods of high cognitive load.
     - **Verification Step (Jidoka):** Verify the sub-agent returns a structured list of detected high-load periods. IF it returns raw unformatted text or an error, request the sub-agent to format the output correctly and retry.
  3. IF high load is detected, Execute the native terminal command `gog calendar create primary --summary "Recovery Block"` to inject "Recovery Block" events to protect decompression time.
     - **Verification Step (Jidoka):** Verify that the `gog calendar create` command returns a successful JSON confirmation. IF it fails, log the failure for that specific block and continue to the next block, rather than halting the entire process.
]

## Expected Output
A JSON log of any recovery blocks injected.
