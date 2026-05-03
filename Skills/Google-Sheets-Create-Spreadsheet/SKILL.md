---
name: google-sheets-create-spreadsheet
description: "Hardened script-based execution for google-sheets-create-spreadsheet."
allowed-tools: [exec]
---

# Google Sheets Create Spreadsheet Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-sheets-create-spreadsheet/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-sheets-create-spreadsheet/scripts/run.sh "arg1" "arg2"`
