---
name: google-contacts-create
description: "Hardened script-based execution for google-contacts-create."
allowed-tools: [exec]
---

# Google Contacts Create Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-contacts-create/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-contacts-create/scripts/run.sh "arg1" "arg2"`
