---
name: gmail-delete-email
description: "Hardened script-based execution for gmail-delete-email."
allowed-tools: [exec]
---

# Gmail Delete Email Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/gmail-delete-email/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/gmail-delete-email/scripts/run.sh "arg1" "arg2"`
