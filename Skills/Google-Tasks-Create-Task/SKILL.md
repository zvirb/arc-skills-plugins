---
name: google-tasks-create-task
description: "Hardened script-based execution for google-tasks-create-task."
allowed-tools: [exec]
---

# Google Tasks Create Task Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-tasks-create-task/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-tasks-create-task/scripts/run.sh "arg1" "arg2"`
