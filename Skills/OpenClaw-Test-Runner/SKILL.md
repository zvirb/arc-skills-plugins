---
name: OpenClaw Test Runner
description: Skill to execute the local OpenClaw regression test suites (batch1 and batch2) and report results.
os: all
requires:
  bins:
    - bash
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** Standardizes the execution of the test suite so it can be triggered autonomously directly from the chat interface, eliminating context switching.
- **Jidoka (自働化):** Evaluates the output logs to determine if any tests failed or panicked.

# OpenClaw Test Runner

This skill allows you to run the local OpenClaw regression test suites (`test_batch1.sh` and `test_batch2.sh`) to verify agent capabilities.

## Cognitive Directives
WHEN [Requested to run tests, execute the test suite, or verify capabilities]
THEN [Execute `bash` using your terminal/shell tool with the path to the requested test script]
AND [Monitor the log file to determine the success or failure of the tests]

**Available Test Suites:**
- Batch 1 (Google Tasks): `/mnt/d/openClaw/Tests/test_batch1.sh` (Logs to `/mnt/d/openClaw/Logs/batch1_results.log`)
- Batch 2 (Google Calendar): `/mnt/d/openClaw/Tests/test_batch2.sh` (Logs to `/mnt/d/openClaw/Logs/batch2_results.log`)

## Schema Example
(Assuming your shell tool accepts a `command` or `script` parameter):
```json
{
  "command": "bash /mnt/d/openClaw/Tests/test_batch2.sh && cat /mnt/d/openClaw/Logs/batch2_results.log"
}
```

## Expected Output
A summary of the test results read from the log file, explicitly stating which tests passed and which failed.
