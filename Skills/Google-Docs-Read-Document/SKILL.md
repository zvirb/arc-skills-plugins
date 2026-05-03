---
name: google-docs-read-document
description: "Hardened script-based execution for google-docs-read-document."
allowed-tools: [exec]
---

# Google Docs Read Document Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-docs-read-document/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-docs-read-document/scripts/run.sh "arg1" "arg2"`
