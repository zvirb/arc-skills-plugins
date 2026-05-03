---
name: google-sheets-update-range
description: "Hardened script-based execution for google-sheets-update-range."
allowed-tools: [exec]
---

# Google Sheets Update Range Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-sheets-update-range/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-sheets-update-range/scripts/run.sh "arg1" "arg2"`
