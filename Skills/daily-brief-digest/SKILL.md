---
name: daily-brief-digest
description: Generates a morning synthesis of emails, calendar, and news.
---

# Daily Brief Digest

This skill directs the agent to compile a multi-source daily status report.

## Execution Directives
1. **Triage Emails:** Execute `himalaya --output json envelope list --page-size 10` to identify urgent messages.
2. **Sync Calendar:** Execute `gog calendar events primary --from "today" --to "today" --json` to fetch the schedule.
3. **Fetch News:** Execute `web_search` for "Top headlines today" to retrieve 3 relevant news summaries.
4. **Generate Report:** 
   - Synthesize the data into a structured Markdown digest.
   - Save the result to `~/.openclaw/cron/DailyDigest_logs/$(date +%F).md` using the `write_file` tool.
5. **Deliver Notification:** Send a summary of the digest to the user's active channel via the `message` tool.

## Expected Output
A structured Markdown digest of the day's priorities and a confirmation of the log file location.
