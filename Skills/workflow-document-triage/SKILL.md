---
name: workflow-document-triage
description: "High-fidelity chained workflow for document search, reading, task creation, and email notification."
allowed-tools: [exec]
---

# Workflow Document Triage Directive

You MUST use the deterministic orchestration script for this complex chain.

## Execution Directives
1. Execute Script:
   - Command: `bash /home/marku/.openclaw/workspace/skills/workflow-document-triage/scripts/triage.sh`
   - Tool: `exec`
2. Report the Verification ID returned by the script.
