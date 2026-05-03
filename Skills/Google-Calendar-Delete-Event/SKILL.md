---
name: google-calendar-delete-event
description: "Hardened script-based execution for google-calendar-delete-event."
allowed-tools: [exec]
---

# Google Calendar Delete Event Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-calendar-delete-event/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-calendar-delete-event/scripts/run.sh "arg1" "arg2"`
