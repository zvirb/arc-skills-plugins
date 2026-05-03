---
name: google-drive-delete-file
description: "Hardened script-based execution for google-drive-delete-file."
allowed-tools: [exec]
---

# Google Drive Delete File Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-drive-delete-file/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-drive-delete-file/scripts/run.sh "arg1" "arg2"`
