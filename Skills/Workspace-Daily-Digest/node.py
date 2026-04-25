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

    prompt = f"""Retrieve today's calendar events, today's active tasks, and recent unread emails. Synthesize a comprehensive morning briefing and write it to a new Google Doc.
    
Context/Arguments: {prompt_args}

You MUST use the provided skills to execute this multi-step workflow. Do not mock the actions.
"""
    print(f"Executing Cross-Service Workflow: Workspace Daily Digest...")
    
    # We rely on OpenClaw's autonomous loop to handle the tool orchestration
    cmd = ["wsl", "--", "bash", "-c", f"openclaw infer '{prompt}' --skills Google-Calendar-Find-Event,Google-Tasks-Find-Tasks,Gmail-Search-Emails,Google-Docs-Create-Document,summarize"]
    
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
