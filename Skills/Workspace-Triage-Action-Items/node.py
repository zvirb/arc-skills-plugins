import sys
import subprocess
import time
import json
import os

def execute_cross_service(arguments_json_str):
    try:
        arguments = json.loads(arguments_json_str)
        prompt_args = " ".join([f"{k}: {v}" for k, v in arguments.items()])
    except:
        prompt_args = arguments_json_str

    prompt = f"""Search for recent unread priority emails. Extract actionable items from them. For each actionable item, create a new task in Google Tasks.
    
Context/Arguments: {prompt_args}

You MUST use the provided skills to execute this multi-step workflow. Do not mock the actions.
"""
    print(f"Executing Cross-Service Workflow: Workspace Triage Action Items...")
    
    # We rely on OpenClaw's autonomous loop to handle the tool orchestration
    cmd = ["wsl", "--", "bash", "-c", f"openclaw infer '{prompt}' --skills Gmail-Search-Emails,Gmail-Retrieve-Email,Google-Tasks-Create-Task"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Workflow failed: {e.stderr}")
        raise Exception("Cross-service workflow execution failed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py '<json_arguments>'")
        sys.exit(1)
    print(execute_cross_service(sys.argv[1]))
