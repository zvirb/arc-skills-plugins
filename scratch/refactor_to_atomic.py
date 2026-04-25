import os
import shutil

# 1. Purge the non-atomic composite and cross-service nodes
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Skills"))
purge_list = [
    "Gmail-Summarize-Email", "Google-Drive-Research-Files", 
    "Google-Contacts-Find-Duplicates", "Google-Drive-Find-Duplicates", 
    "Google-Calendar-Find-Conflicts", "Workspace-Audit-Missing-Meetings",
    "Workspace-Generate-Project-Brief", "Workspace-Triage-Action-Items",
    "Workspace-Invoice-Extraction", "Workspace-Meeting-Preparation",
    "Workspace-Contact-Enrichment", "Workspace-Daily-Digest",
    "Workspace-Draft-Meeting-Followup", "Workspace-Find-Inbox-Zero-Anomalies",
    "Workspace-Proactive-Rescheduler"
]

for d in purge_list:
    path = os.path.join(base_dir, d)
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Purged monolithic skill: {d}")

# 2. Generate new LLM-Transformer Sub-Nodes
LLM_NODES = [
    {"name": "LLM Extract JSON", "dir": "LLM-Extract-JSON", "desc": "Extract strictly formatted JSON from raw text.", "validation": "dict"},
    {"name": "LLM Extract Action Items", "dir": "LLM-Extract-Action-Items", "desc": "Extract a list of actionable tasks from raw text.", "validation": "list"},
    {"name": "LLM Find Duplicates", "dir": "LLM-Find-Duplicates", "desc": "Identify duplicates in a dataset and return a list.", "validation": "list"},
    {"name": "LLM Identify Conflicts", "dir": "LLM-Identify-Conflicts", "desc": "Identify time conflicts in a calendar dataset and return a list.", "validation": "list"},
    {"name": "LLM Summarize Text", "dir": "LLM-Summarize-Text", "desc": "Summarize raw text, returning a structured summary object.", "validation": "dict"}
]

SKILL_TEMPLATE = """---
name: {name}
description: Atomic transformation node to {desc_lower} Loops internally until successful.
os: windows
requires:
  bins:
    - python
    - openclaw
---

# {name}

## Role
You are a precise data transformation node. Your only responsibility is to {desc_lower}

## Input
A JSON object containing {{ "text": "raw content to process", "schema": "optional json schema description" }}.

## Expected Output
A JSON {output_type} representing the result of the operation.
"""

NODE_TEMPLATE = """import sys
import json
import time
import subprocess

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
        arguments = {{"text": arguments_json_str}} # Fallback if passed raw string

    raw_text = arguments.get("text", "")
    schema_hint = arguments.get("schema", "A valid JSON {output_shape}")
    
    # Safely escape text for the shell command
    safe_text = raw_text.replace("'", "").replace('"', '')[:3000]

    prompt = f"Analyze the following text and output ONLY valid JSON matching this schema/intent: {{schema_hint}}.\\n\\nText: {{safe_text}}"

    for attempt in range(1, max_retries + 1):
        print(f"Attempt {{attempt}}: Executing {name} transformation...")
        try:
            cmd = ["wsl", "--", "bash", "-c", f"openclaw infer '{{prompt}}'"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # The LLM might wrap output in markdown ```json ... ```. Strip it.
            clean_out = result.stdout.strip()
            if clean_out.startswith("```json"):
                clean_out = clean_out[7:]
            if clean_out.startswith("```"):
                clean_out = clean_out[3:]
            if clean_out.endswith("```"):
                clean_out = clean_out[:-3]
            clean_out = clean_out.strip()

            if validate_output(clean_out):
                return json.loads(clean_out)
        except Exception as e:
            print(f"OpenClaw Inference failed on attempt {{attempt}}: {{e}}")
            
        print("Validation failed or LLM hallucinated format. Retrying...")
        time.sleep(2)
        
    raise Exception("Failed to achieve valid JSON schema after max retries.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py '<json_arguments>'")
        sys.exit(1)
    print(json.dumps(execute_node(sys.argv[1]), indent=2))
"""

for node in LLM_NODES:
    skill_dir = os.path.join(base_dir, node["dir"])
    os.makedirs(skill_dir, exist_ok=True)
    
    desc_lower = node["desc"].lower()
    if not desc_lower.endswith("."): desc_lower += "."
    
    output_shape = "array ([...])" if node["validation"] == "list" else "object ({...})"
    
    skill_content = SKILL_TEMPLATE.format(
        name=node["name"],
        desc_lower=desc_lower,
        output_type="array" if node["validation"] == "list" else "object"
    )
    with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
        f.write(skill_content)
        
    node_content = NODE_TEMPLATE.format(
        name=node["name"],
        validation_type=node["validation"],
        output_shape=output_shape
    )
    with open(os.path.join(skill_dir, "node.py"), "w") as f:
        f.write(node_content)

print(f"Successfully generated {len(LLM_NODES)} LLM Transformer Sub-Nodes.")
