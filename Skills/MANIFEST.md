# OpenClaw Skill Manifest

| Skill Name | Description |
| :--- | :--- |
| agents | Design, build, and deploy AI agents with architecture patterns, framework selection, memory systems, and production safety. |
| backlog-grooming | Atomic node skill to autonomously manage stale items in Google Tasks. |
| calendar-guard | Atomic node skill to defend the schedule by injecting recovery blocks. |
| capture-classification | Semantic router for unstructured audio transcripts or notes. |
| clauditor | Tamper-resistant audit watchdog for Clawdbot agents. Detects and logs suspicious filesystem activity with HMAC-chained evidence. |
| clawcoach-core | Data-driven AI health coach execution skill. |
| clawcoach-setup | One-time setup for ClawCoach AI health coaching. |
| composio-integration | Unified API skill for 600+ apps. Currently enabled for Gmail and Google Tasks. |
| crm-entity-extraction | Atomic node skill to extract CRM data from text and append to Google Sheets. |
| daily-brief-digest | Generates a morning synthesis of emails, calendar, and news. |
| executive-assistant-time-blocking | High-level orchestration skill to block out time for tasks. |
| flow-state-monitoring | Workflow-driven skill that infers deep focus and autonomously mutes interruptions. |
| gemini-web-search | Use Gemini CLI to perform web searches and fact-finding. |
| gmail-delete-email | Hardened script-based execution for gmail-delete-email. |
| gmail-draft-email | Hardened script-based execution for gmail-draft-email. |
| gmail-modify-labels | Hardened script-based execution for gmail-modify-labels. |
| gmail-retrieve-email | Hardened script-based execution for gmail-retrieve-email. |
| gmail-search-emails | Hardened script-based execution for gmail-search-emails. |
| gmail-send-email | Hardened script-based execution for gmail-send-email. |
| gog | Triggers for generic Google Workspace queries (Drive, Sheets, Docs, Contacts). Enforces third-person imperative logic. |
| google-calendar-create-event | Hardened script-based execution for google-calendar-create-event. |
| google-calendar-delete-event | Hardened script-based execution for google-calendar-delete-event. |
| google-calendar-find-event | Hardened script-based execution for google-calendar-find-event. |
| google-calendar-update-event | Hardened script-based execution for google-calendar-update-event. |
| google-contacts-create | Hardened script-based execution for google-contacts-create. |
| google-contacts-search | Hardened script-based execution for google-contacts-search. |
| google-docs-create-document | Hardened script-based execution for google-docs-create-document. |
| google-docs-read-document | Hardened script-based execution for google-docs-read-document. |
| google-docs-update-document | Hardened script-based execution for google-docs-update-document. |
| google-drive-delete-file | Hardened script-based execution for google-drive-delete-file. |
| google-drive-download-file | Hardened script-based execution for google-drive-download-file. |
| google-drive-search | Hardened script-based execution for google-drive-search. |
| google-drive-search-files | Hardened script-based execution for google-drive-search-files. |
| google-drive-share-file | Hardened script-based execution for google-drive-share-file. |
| google-drive-upload-file | Hardened script-based execution for google-drive-upload-file. |
| google-sheets-append-row | Hardened script-based execution for google-sheets-append-row. |
| google-sheets-create-spreadsheet | Hardened script-based execution for google-sheets-create-spreadsheet. |
| google-sheets-read-range | Hardened script-based execution for google-sheets-read-range. |
| google-sheets-update-range | Hardened script-based execution for google-sheets-update-range. |
| google-tasks-complete-task | Hardened script-based execution for google-tasks-complete-task. |
| google-tasks-create-task | Hardened script-based execution for google-tasks-create-task. |
| google-tasks-find-tasks | Hardened script-based execution for google-tasks-find-tasks. |
| google-tasks-update-task | Hardened script-based execution for google-tasks-update-task. |
| llm-analyze-flow-state | Atomic transformation node to analyze telemetry and infer if the user is in a deep focus flow state. Loops internally until successful. |
| llm-classify-intent | Atomic node to classify the intent and urgency of text. |
| llm-extract-action-items | Atomic transformation node to extract a list of actionable tasks from raw text. Loops internally until successful. |
| llm-extract-json | Atomic node to extract strictly formatted JSON from raw text. |
| llm-find-duplicates | Atomic transformation node to identify duplicates in a dataset and return a list. Loops internally until successful. |
| llm-identify-conflicts | Atomic transformation node to identify time conflicts in a calendar dataset and return a list. Loops internally until successful. |
| llm-refine-tool-use | Teaches the agent to use the ToolStrategyEngine plugin to check for tool constraints before executing complex tools, and to record failures to prevent future hallucinations. |
| llm-select-random-item | Atomic transformation node to select a random item from a provided list. Loops internally until successful. |
| llm-summarize-text | Atomic node to generate concise summaries of text. |
| meeting-to-action | Convert meeting notes or transcripts into clear summaries, decisions, and action items with owners and due dates. Use when a user asks to turn a meeting recording, transcript, or notes into a follow-up plan. |
| memu | > |
| micro-suck-generation | Workflow-driven skill that issues minor resilience challenges to build task-initiation momentum. |
| nxt-pulse-agent | Proactive productivity skill with ADHD micro-stepping support. |
| open-prose | OpenProse VM orchestrator for multi-agent workflows. |
| pg | Write efficient PostgreSQL queries and design schemas with proper indexing and patterns. |
| process-braindump | Triggers for processing unstructured thoughts. Prioritizes, decomposes, and routes content. |
| process-journal | Triggers for processing handwritten meeting notes or journal entries. Performs timestamped appends. |
| process-schematics | Triggers for processing design changes, measurements, and diagrams. Preserves original design state. |
| process-tasks | Triggers for processing handwritten todo lists. Performs delta-check and non-destructive appends. |
| redis-store | Use Redis effectively for caching, queues, and data structures with proper expiration and persistence. |
| root-router | Master routing skill for the OpenClaw high-fidelity library. Directs intent to specific sub-skills using dynamic loading. |
| vague-task-decomposition | Atomic node to break complex tasks into actionable subtasks. |
| vector-store-upsert-memory | Atomic node skill to upsert text/metadata into the local vector store (LanceDB). Loops internally until successful. |
| workflow-document-triage | High-fidelity chained workflow for document search, reading, task creation, and email notification. |
