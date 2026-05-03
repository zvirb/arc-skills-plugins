---
name: gmail-send-email
description: "Hardened script-based execution for gmail-send-email."
allowed-tools: [exec]
---

# Gmail Send Email Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/gmail-send-email/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/gmail-send-email/scripts/run.sh "arg1" "arg2"`
