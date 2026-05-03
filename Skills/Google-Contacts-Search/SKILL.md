---
name: google-contacts-search
description: "Hardened script-based execution for google-contacts-search."
allowed-tools: [exec]
---

# Google Contacts Search Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-contacts-search/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-contacts-search/scripts/run.sh "arg1" "arg2"`
