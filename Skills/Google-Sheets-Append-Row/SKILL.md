---
name: google-sheets-append-row
description: "Hardened script-based execution for google-sheets-append-row."
allowed-tools: [exec]
---

# Google Sheets Append Row Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-sheets-append-row/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-sheets-append-row/scripts/run.sh "arg1" "arg2"`
