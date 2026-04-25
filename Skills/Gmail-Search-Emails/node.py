import sys
import json
import time
import subprocess
import os

try:
    from composio import Composio
except ImportError:
    Composio = None

def validate_emails(output_str):
    try:
        data = json.loads(output_str) if isinstance(output_str, str) else output_str
        return isinstance(data, list)
    except:
        return False

def search_emails(query, max_retries=3):
    composio_api_key = os.environ.get("COMPOSIO_API_KEY")
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}: Searching emails for '{query}'...")
        try:
            # Try native gog
            cmd = ["wsl", "--", "bash", "-c", f"gog gmail search '{query}' --json"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if validate_emails(result.stdout):
                return json.loads(result.stdout)
        except Exception as e:
            print(f"gog tool failed on attempt {attempt}: {e}")
            
        # Try fallback
        try:
            if Composio:
                client = Composio(api_key=composio_api_key)
                res = client.tools.execute("GMAIL_SEARCH", arguments={"query": query})
                if res.successful and validate_emails(res.data):
                    return res.data
        except Exception as e:
            print(f"Fallback composio failed on attempt {attempt}: {e}")
            
        print("Validation failed or tools errored. Retrying...")
        time.sleep(2)
        
    raise Exception("Failed to achieve expected outcome after max retries.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py '<query>'")
        sys.exit(1)
    print(json.dumps(search_emails(sys.argv[1]), indent=2))
