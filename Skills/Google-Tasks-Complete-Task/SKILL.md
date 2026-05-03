---
name: google-tasks-complete-task
description: "Hardened script-based execution for google-tasks-complete-task."
allowed-tools: [exec]
---

# Google Tasks Complete Task Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-tasks-complete-task/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-tasks-complete-task/scripts/run.sh "arg1" "arg2"`
