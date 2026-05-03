---
name: google-tasks-find-tasks
description: "Hardened script-based execution for google-tasks-find-tasks."
allowed-tools: [exec]
---

# Google Tasks Find Tasks Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-tasks-find-tasks/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-tasks-find-tasks/scripts/run.sh "arg1" "arg2"`
