---
name: gmail-search-emails
description: "Hardened script-based execution for gmail-search-emails."
allowed-tools: [exec]
---

# Gmail Search Emails Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/gmail-search-emails/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/gmail-search-emails/scripts/run.sh "arg1" "arg2"`
