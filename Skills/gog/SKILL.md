---
name: gog
description: "Workspace core (Drive, Sheets, Docs, Contacts). Note: Tasks and Calendar are handled by the bundled gog skill."
allowed-tools: [gog, exec]
triggers: [google sheets, spreadsheet, drive search, file search, list contacts]
negative-triggers: [create event, find event, schedule meeting, delete event, list calendar, send email, search email]
---

> [!NOTE]
> This workspace override explicitly excludes **Tasks** and **Calendar** to prevent shadowing the optimized bundled `gog` logic.

# Generic GOG Directive

This skill directs the agent to manage non-calendar/non-email Workspace tasks.

## Execution Directives
1. **Identify Tool Subset:** Determine if the request targets `Drive`, `Sheets`, `Docs`, or `Contacts`.
2. **Format Command:** Construct the `gog` CLI command string using the `--json` flag for deterministic parsing.
3. **Verify Context:** Before executing, ensure `GOG_ACCOUNT` is set in the environment.
4. **Execute & Parse:** Run the command using the `exec` tool. Parse the JSON result and present a summary to the user.

## Expected Output
A JSON summary or formatted list of files, spreadsheet rows, or contacts.
