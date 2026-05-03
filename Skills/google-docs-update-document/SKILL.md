---
name: google-docs-update-document
description: "Hardened script-based execution for google-docs-update-document."
allowed-tools: [exec]
---

# Google Docs Update Document Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-docs-update-document/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-docs-update-document/scripts/run.sh "arg1" "arg2"`
