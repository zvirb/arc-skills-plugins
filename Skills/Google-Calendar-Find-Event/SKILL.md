---
name: google-calendar-find-event
description: "Hardened script-based execution for google-calendar-find-event."
allowed-tools: [exec]
---

# Google Calendar Find Event Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-calendar-find-event/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-calendar-find-event/scripts/run.sh "arg1" "arg2"`
