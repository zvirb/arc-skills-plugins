---
name: google-drive-share-file
description: "Hardened script-based execution for google-drive-share-file."
allowed-tools: [exec]
---

# Google Drive Share File Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-drive-share-file/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-drive-share-file/scripts/run.sh "arg1" "arg2"`
