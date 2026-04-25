import sys
import json
import time
import subprocess
import os

try:
    from composio import Composio
except ImportError:
    Composio = None

def validate_events(output_str):
    try:
        data = json.loads(output_str)
        return isinstance(data, list)
    except:
        return False

def find_event(query, max_retries=3):
    composio_api_key = os.environ.get("COMPOSIO_API_KEY")
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}: Searching events for '{query}'...")
        try:
            # Try native gog
            cmd = ["wsl", "--", "bash", "-c", f"gog calendar list --query='{query}' --json"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if validate_events(result.stdout):
                return json.loads(result.stdout)
        except Exception as e:
            print(f"gog tool failed on attempt {attempt}: {e}")
            
        # Try fallback
        try:
            if Composio:
                client = Composio(api_key=composio_api_key)
                res = client.tools.execute("GOOGLECALENDAR_FIND_EVENT", arguments={"query": query})
                if res.successful and isinstance(res.data, list):
                    return res.data
        except Exception as e:
            print(f"Fallback composio failed on attempt {attempt}: {e}")
            
        print("Validation failed or tools errored. Retrying...")
        time.sleep(2)
        
    raise Exception("Failed to achieve expected outcome after max retries.")

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "meeting"
    print(json.dumps(find_event(query), indent=2))
