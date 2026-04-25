import sys
import json
import time
import subprocess
import os

def validate_output(output_str):
    try:
        data = json.loads(output_str) if isinstance(output_str, str) else output_str
        return isinstance(data, dict) and "status" in data
    except:
        return False

def execute_node(arguments_json_str, max_retries=3):
    try:
        arguments = json.loads(arguments_json_str)
    except:
        arguments = {"text": arguments_json_str}

    text = arguments.get("text", "")
    metadata = arguments.get("metadata", {})
    
    # We use openclaw memory tool or a custom lancedb script via wsl
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}: Upserting to Vector Store...")
        try:
            # Example using a placeholder CLI command for lancedb
            # In a real implementation, this would call a python script in WSL that uses lancedb SDK
            cmd = ["wsl", "--", "bash", "-c", f"openclaw memory add --text='{text}' --json"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if validate_output(result.stdout):
                return json.loads(result.stdout)
        except Exception as e:
            print(f"Upsert failed on attempt {attempt}: {e}")
            
        print("Validation failed or database errored. Retrying...")
        time.sleep(2)
        
    raise Exception("Failed to achieve expected outcome after max retries.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py '<json_arguments>'")
        sys.exit(1)
    print(json.dumps(execute_node(sys.argv[1]), indent=2))
