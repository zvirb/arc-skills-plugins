import os
import json

NODES = [
    # Gmail
    {"name": "Gmail Send Email", "dir": "Gmail-Send-Email", "desc": "Send a new email.", "gog_cmd": "gmail send", "composio_tool": "GMAIL_SEND_EMAIL", "validation": "dict"},
    {"name": "Gmail Draft Email", "dir": "Gmail-Draft-Email", "desc": "Draft a new email.", "gog_cmd": "gmail draft", "composio_tool": "GMAIL_CREATE_DRAFT", "validation": "dict"},
    {"name": "Gmail Delete Email", "dir": "Gmail-Delete-Email", "desc": "Delete an email by ID.", "gog_cmd": "gmail delete", "composio_tool": "GMAIL_DELETE_MESSAGE", "validation": "dict"},
    {"name": "Gmail Modify Labels", "dir": "Gmail-Modify-Labels", "desc": "Modify labels of an email.", "gog_cmd": "gmail modify", "composio_tool": "GMAIL_MODIFY_MESSAGE", "validation": "dict"},
    
    # Calendar
    {"name": "Google Calendar Update Event", "dir": "Google-Calendar-Update-Event", "desc": "Update an existing calendar event.", "gog_cmd": "calendar update", "composio_tool": "GOOGLECALENDAR_UPDATE_EVENT", "validation": "dict"},
    {"name": "Google Calendar Delete Event", "dir": "Google-Calendar-Delete-Event", "desc": "Delete a calendar event.", "gog_cmd": "calendar delete", "composio_tool": "GOOGLECALENDAR_DELETE_EVENT", "validation": "dict"},
    
    # Drive
    {"name": "Google Drive Upload File", "dir": "Google-Drive-Upload-File", "desc": "Upload a file to Google Drive.", "gog_cmd": "drive upload", "composio_tool": "GOOGLEDRIVE_UPLOAD_FILE", "validation": "dict"},
    {"name": "Google Drive Download File", "dir": "Google-Drive-Download-File", "desc": "Download a file from Google Drive.", "gog_cmd": "drive download", "composio_tool": "GOOGLEDRIVE_DOWNLOAD_FILE", "validation": "dict"},
    {"name": "Google Drive Delete File", "dir": "Google-Drive-Delete-File", "desc": "Delete a file from Google Drive.", "gog_cmd": "drive delete", "composio_tool": "GOOGLEDRIVE_DELETE_FILE", "validation": "dict"},
    {"name": "Google Drive Share File", "dir": "Google-Drive-Share-File", "desc": "Share a file in Google Drive.", "gog_cmd": "drive share", "composio_tool": "GOOGLEDRIVE_CREATE_PERMISSION", "validation": "dict"},
    {"name": "Google Drive Search Files", "dir": "Google-Drive-Search-Files", "desc": "Search for files in Google Drive.", "gog_cmd": "drive search", "composio_tool": "GOOGLEDRIVE_SEARCH", "validation": "list"},
    
    # Docs
    {"name": "Google Docs Create Document", "dir": "Google-Docs-Create-Document", "desc": "Create a new Google Document.", "gog_cmd": "docs create", "composio_tool": "GOOGLEDOCS_CREATE_DOCUMENT", "validation": "dict"},
    {"name": "Google Docs Read Document", "dir": "Google-Docs-Read-Document", "desc": "Read the contents of a Google Document.", "gog_cmd": "docs read", "composio_tool": "GOOGLEDOCS_GET_DOCUMENT", "validation": "dict"},
    {"name": "Google Docs Update Document", "dir": "Google-Docs-Update-Document", "desc": "Update the contents of a Google Document.", "gog_cmd": "docs update", "composio_tool": "GOOGLEDOCS_UPDATE_DOCUMENT", "validation": "dict"},
    
    # Sheets
    {"name": "Google Sheets Create Spreadsheet", "dir": "Google-Sheets-Create-Spreadsheet", "desc": "Create a new Google Spreadsheet.", "gog_cmd": "sheets create", "composio_tool": "GOOGLESHEETS_CREATE_SPREADSHEET", "validation": "dict"},
    {"name": "Google Sheets Read Range", "dir": "Google-Sheets-Read-Range", "desc": "Read a range of values from a Spreadsheet.", "gog_cmd": "sheets read", "composio_tool": "GOOGLESHEETS_GET_VALUES", "validation": "dict"},
    {"name": "Google Sheets Update Range", "dir": "Google-Sheets-Update-Range", "desc": "Update a range of values in a Spreadsheet.", "gog_cmd": "sheets update", "composio_tool": "GOOGLESHEETS_UPDATE_VALUES", "validation": "dict"},
    {"name": "Google Sheets Append Row", "dir": "Google-Sheets-Append-Row", "desc": "Append a row to a Spreadsheet.", "gog_cmd": "sheets append", "composio_tool": "GOOGLESHEETS_APPEND_VALUES", "validation": "dict"},
    
    # Tasks
    {"name": "Google Tasks Find Tasks", "dir": "Google-Tasks-Find-Tasks", "desc": "Find active tasks in Google Tasks.", "gog_cmd": "tasks list", "composio_tool": "GOOGLETASKS_LIST_TASKS", "validation": "list"},
    {"name": "Google Tasks Create Task", "dir": "Google-Tasks-Create-Task", "desc": "Create a new task in Google Tasks.", "gog_cmd": "tasks create", "composio_tool": "GOOGLETASKS_CREATE_TASK", "validation": "dict"},
    {"name": "Google Tasks Update Task", "dir": "Google-Tasks-Update-Task", "desc": "Update an existing task in Google Tasks.", "gog_cmd": "tasks update", "composio_tool": "GOOGLETASKS_UPDATE_TASK", "validation": "dict"},
    {"name": "Google Tasks Complete Task", "dir": "Google-Tasks-Complete-Task", "desc": "Mark a task as complete.", "gog_cmd": "tasks complete", "composio_tool": "GOOGLETASKS_COMPLETE_TASK", "validation": "dict"},

    # Contacts
    {"name": "Google Contacts Search", "dir": "Google-Contacts-Search", "desc": "Search Google Contacts.", "gog_cmd": "contacts search", "composio_tool": "GOOGLECONTACTS_SEARCH_CONTACTS", "validation": "list"},
    {"name": "Google Contacts Create", "dir": "Google-Contacts-Create", "desc": "Create a new Google Contact.", "gog_cmd": "contacts create", "composio_tool": "GOOGLECONTACTS_CREATE_CONTACT", "validation": "dict"}
]

SKILL_TEMPLATE = """---
name: {name}
description: Atomic node skill to {desc_lower} Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - gog
  env:
    - COMPOSIO_API_KEY
---

# {name}

## Role
You are a precise tool orchestration node. Your only responsibility is to {desc_lower}

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON {output_type} representing the result of the operation.
"""

NODE_TEMPLATE = """import sys
import json
import time
import subprocess
import os

try:
    from composio import Composio
except ImportError:
    Composio = None

def validate_output(output_str):
    try:
        data = json.loads(output_str) if isinstance(output_str, str) else output_str
        return isinstance(data, {validation_type})
    except:
        return False

def execute_node(arguments_json_str, max_retries=3):
    try:
        arguments = json.loads(arguments_json_str)
    except:
        arguments = {{"query": arguments_json_str}} # Fallback if passed raw string

    composio_api_key = os.environ.get("COMPOSIO_API_KEY")
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {{attempt}}: Executing {name}...")
        
        # Try native gog
        try:
            # Flatten args for basic CLI
            cli_args = " ".join([f"--{{k}}='{{v}}'" for k, v in arguments.items()])
            cmd = ["wsl", "--", "bash", "-c", f"gog {gog_cmd} {{cli_args}} --json"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if validate_output(result.stdout):
                return json.loads(result.stdout)
        except Exception as e:
            print(f"gog tool failed on attempt {{attempt}}: {{e}}")
            
        # Try fallback composio
        try:
            if Composio:
                client = Composio(api_key=composio_api_key)
                res = client.tools.execute("{composio_tool}", arguments=arguments)
                if res.successful and validate_output(res.data):
                    return res.data
        except Exception as e:
            print(f"Fallback composio failed on attempt {{attempt}}: {{e}}")
            
        print("Validation failed or tools errored. Retrying...")
        time.sleep(2)
        
    raise Exception("Failed to achieve expected outcome after max retries.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py '<json_arguments>'")
        sys.exit(1)
    print(json.dumps(execute_node(sys.argv[1]), indent=2))
"""

def generate():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Skills"))
    for node in NODES:
        skill_dir = os.path.join(base_dir, node["dir"])
        os.makedirs(skill_dir, exist_ok=True)
        
        # Write SKILL.md
        desc_lower = node["desc"].lower()
        if not desc_lower.endswith("."): desc_lower += "."
        
        skill_content = SKILL_TEMPLATE.format(
            name=node["name"],
            desc_lower=desc_lower,
            output_type="array" if node["validation"] == "list" else "object"
        )
        with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
            f.write(skill_content)
            
        # Write node.py
        node_content = NODE_TEMPLATE.format(
            name=node["name"],
            validation_type=node["validation"],
            gog_cmd=node["gog_cmd"],
            composio_tool=node["composio_tool"]
        )
        with open(os.path.join(skill_dir, "node.py"), "w") as f:
            f.write(node_content)
            
    print(f"Successfully generated {len(NODES)} atomic nodes in Skills directory.")

if __name__ == "__main__":
    generate()
