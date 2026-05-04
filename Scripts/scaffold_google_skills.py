import os
import json

SKILLS = [
    # Gmail
    ("gmail-delete-email", "gog gmail trash \"$1\" --force --json"),
    ("gmail-draft-email", "gog gmail drafts create --to \"$1\" --subject \"$2\" --body \"$3\" --json"),
    ("gmail-modify-labels", "gog gmail modify \"$1\" --add \"$2\" --remove \"$3\" --json"),
    ("gmail-retrieve-email", "gog gmail messages get \"$1\" --json"),
    ("gmail-search-emails", "gog gmail search \"$1\" --json"),
    ("gmail-send-email", "gog gmail send --to \"$1\" --subject \"$2\" --body \"$3\" --json"),
    # Calendar
    ("google-calendar-create-event", "gog calendar create primary --summary \"$1\" --from \"$2\" --to \"$3\" --json"),
    ("google-calendar-delete-event", "gog calendar delete primary \"$1\" --force --json"),
    ("google-calendar-find-event", "gog calendar list --json"),
    ("google-calendar-update-event", "gog calendar update primary \"$1\" --summary \"$2\" --force --json"),
    # Contacts
    ("google-contacts-create", "gog contacts create --given-name \"$1\" --email \"$2\" --json"),
    ("google-contacts-search", "gog contacts search \"$1\" --json"),
    # Docs
    ("google-docs-create-document", "gog docs create \"$1\" --json"),
    ("google-docs-read-document", "gog docs get \"$1\" --json"),
    ("google-docs-update-document", "gog docs update \"$1\" --text \"$2\" --append --json"),
    # Drive
    ("google-drive-delete-file", "gog drive delete \"$1\" --force --json"),
    ("google-drive-download-file", "gog drive download \"$1\" \"$2\""),
    ("google-drive-search", "gog drive ls --json"),
    ("google-drive-search-files", "gog drive ls --json"),
    ("google-drive-share-file", "gog drive share \"$1\" --role reader --type anyone --json"),
    ("google-drive-upload-file", "gog drive upload \"$1\" --json"),
    # Sheets
    ("google-sheets-append-row", "gog sheets append \"$1\" \"$2\" --values \"$3\" --json"),
    ("google-sheets-create-spreadsheet", "gog sheets create \"$1\" --json"),
    ("google-sheets-read-range", "gog sheets get \"$1\" \"$2\" --json"),
    ("google-sheets-update-range", "gog sheets update \"$1\" \"$2\" --values \"$3\" --json"),
    # Tasks
    ("google-tasks-complete-task", "gog tasks complete @default \"$1\" --json"),
    ("google-tasks-create-task", "gog tasks add @default --title \"$1\" --json"),
    ("google-tasks-find-tasks", "gog tasks list @default --json"),
    ("google-tasks-update-task", "gog tasks update @default \"$1\" --title \"$2\" --json"),
]

WORKSPACE = "/home/marku/.openclaw/workspace/skills"
BIN_PATH = "/home/marku/.local/bin"

for skill_name, cmd in SKILLS:
    skill_dir = os.path.join(WORKSPACE, skill_name)
    scripts_dir = os.path.join(skill_dir, "scripts")
    
    if not os.path.exists(skill_dir):
        os.makedirs(skill_dir)
        
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
        
    script_path = os.path.join(scripts_dir, "run.sh")
    with open(script_path, "w") as f:
        f.write(f"#!/bin/bash\n{BIN_PATH}/{cmd}\n")
    os.chmod(script_path, 0o755)
    
    # Write SKILL.md
    skill_md = f"""---
name: {skill_name}
description: "Hardened script-based execution for {skill_name}."
allowed-tools: [exec]
---

# {skill_name.replace('-', ' ').title()} Directive

You MUST use the deterministic script for this action.

## Execution Directives
1. Execute Script:
   - Command: `bash {script_path}` followed by required arguments in double quotes.
   - Tool: `exec`
   - Details: Pass arguments sequentially. Example: `bash {script_path} "arg1" "arg2"`
"""
    with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
        f.write(skill_md)

print("Scaffolded 29 Google Workspace skills successfully.")
