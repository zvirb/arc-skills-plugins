---
name: google-drive-search-files
description: "Hardened script-based execution for google-drive-search-files."
allowed-tools: [exec]
---

# Google Drive Search Files Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-drive-search-files/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-drive-search-files/scripts/run.sh "arg1" "arg2"`
