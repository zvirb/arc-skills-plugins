---
name: backlog-grooming
description: Atomic node skill to autonomously manage stale items in Google Tasks.
os: all
requires:
  bins: []
---

# Backlog Grooming

This skill directs the agent to trigger the native programmatic backlog grooming plugin.

## Execution Directives
1. **Initiate Grooming:** Execute the `workflow_backlog_grooming` plugin tool with empty JSON `{}`.
2. **Verify Response:** Inspect the tool output for a valid JSON object.
3. **Handle Errors:** If the tool returns an error or hallucinated output, report the issue to the user. Wait 3 seconds and retry (maximum 3 attempts).
4. **Finalize:** Report the JSON summary of groomed tasks to the user once successful.

## Expected Output
A JSON summary of the groomed tasks returned by the plugin.
