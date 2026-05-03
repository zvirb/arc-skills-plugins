---
name: google-docs-create-document
description: "Hardened script-based execution for google-docs-create-document."
allowed-tools: [exec]
---

# Google Docs Create Document Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/google-docs-create-document/scripts/run.sh` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash /home/marku/.openclaw/workspace/skills/google-docs-create-document/scripts/run.sh "arg1" "arg2"`
