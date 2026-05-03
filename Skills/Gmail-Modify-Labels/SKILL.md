---
name: gmail-modify-labels
description: "Hardened script-based execution for gmail-modify-labels."
allowed-tools: [exec]
---

# Gmail Modify Labels Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/gmail-modify-labels/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/gmail-modify-labels/scripts/run.sh "arg1" "arg2"`
