---
name: kebab-case-auto-fix
description: Unified API skill for 600+ apps. Currently enabled for Gmail and Google Tasks.
metadata:
  openclaw: {"requires": {"env": ["COMPOSIO_API_KEY"]}}
---

# Composio Integration

This skill directs the agent to execute cross-app actions via the Composio unified API.

## Execution Directives
1. **Identify Tool:** Map the user request to a Composio tool slug (e.g., `GMAIL_SEND_EMAIL`, `GOOGLETASKS_INSERT_TASK`).
2. **Verify Account:** Ensure the correct `account_id` is used (Gmail: `ca_0cxayHx2BME1`, Tasks: `ca_kSNnWG4OHngG`).
3. **Format Request:** Prepare the parameters JSON for the `execute-tool.mjs` script.
4. **Request Approval:** For any destructive or external-facing action (sending mail, deleting tasks), present the action and parameters to the user for approval.
5. **Execute Action:** Run `node scripts/execute-tool.mjs <TOOL_SLUG> <ACCOUNT_ID> '<PARAMS_JSON>'`.
6. **Report Result:** Provide the raw tool output or a summarized success message to the user.

## Expected Output
A JSON result from the Composio API confirming the action's status.
