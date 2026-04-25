import sys
import json
import time
import subprocess
import os

try:
    from composio import Composio
except ImportError:
    Composio = None

def execute_composite(arguments_json_str, max_retries=3):
    try:
        arguments = json.loads(arguments_json_str)
    except:
        arguments = {"query": arguments_json_str} # Fallback

    composio_api_key = os.environ.get("COMPOSIO_API_KEY")
    
    print(f"Step 1: Fetching raw data for Google Drive Find Duplicates...")
    raw_data = None
    try:
        cli_args = " ".join([f"--{k}='{v}'" for k, v in arguments.items()])
        cmd = ["wsl", "--", "bash", "-c", f"gog drive search {cli_args} --json"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        raw_data = result.stdout
    except Exception as e:
        print(f"gog fetch failed: {e}")
        if Composio:
            client = Composio(api_key=composio_api_key)
            res = client.tools.execute("GOOGLEDRIVE_SEARCH", arguments=arguments)
            if res.successful:
                raw_data = json.dumps(res.data)

    if not raw_data:
        raise Exception("Failed to fetch prerequisite data for composite action.")

    print(f"Step 2: Processing data through OpenClaw skills (summarize)...")
    for attempt in range(1, max_retries + 1):
        try:
            # We pass the raw data as a string to openclaw infer (safely truncated to avoid arg too long)
            safe_data = raw_data.replace("'", "").replace('"', '')[:2000]
            prompt = f"List all identical or duplicate files from this payload based on name/size: {safe_data}"
            
            infer_cmd = ["wsl", "--", "bash", "-c", f"openclaw infer '{prompt}' --skills summarize"]
            res = subprocess.run(infer_cmd, capture_output=True, text=True, check=True)
            return res.stdout
        except Exception as e:
            print(f"OpenClaw Inference failed on attempt {attempt}: {e}")
            time.sleep(2)
            
    raise Exception("Failed to achieve composite outcome after max retries.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py '<json_arguments>'")
        sys.exit(1)
    print(execute_composite(sys.argv[1]))
