import sys
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
        return isinstance(data, dict)
    except:
        return False

def execute_node(arguments_json_str, max_retries=3):
    try:
        arguments = json.loads(arguments_json_str)
    except:
        arguments = {"query": arguments_json_str} # Fallback if passed raw string

    composio_api_key = os.environ.get("COMPOSIO_API_KEY")
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}: Executing Google Drive Download File...")
        
        # Try native gog
        try:
            # Flatten args for basic CLI
            cli_args = " ".join([f"--{k}='{v}'" for k, v in arguments.items()])
            cmd = ["wsl", "--", "bash", "-c", f"gog drive download {cli_args} --json"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if validate_output(result.stdout):
                return json.loads(result.stdout)
        except Exception as e:
            print(f"gog tool failed on attempt {attempt}: {e}")
            
        # Try fallback composio
        try:
            if Composio:
                client = Composio(api_key=composio_api_key)
                res = client.tools.execute("GOOGLEDRIVE_DOWNLOAD_FILE", arguments=arguments)
                if res.successful and validate_output(res.data):
                    return res.data
        except Exception as e:
            print(f"Fallback composio failed on attempt {attempt}: {e}")
            
        print("Validation failed or tools errored. Retrying...")
        time.sleep(2)
        
    raise Exception("Failed to achieve expected outcome after max retries.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py '<json_arguments>'")
        sys.exit(1)
    print(json.dumps(execute_node(sys.argv[1]), indent=2))
