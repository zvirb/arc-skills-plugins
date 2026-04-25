import sys
import json
import time
import subprocess
import os

try:
    from composio import Composio
except ImportError:
    Composio = None

def validate_creation(output_str):
    try:
        data = json.loads(output_str) if isinstance(output_str, str) else output_str
        return isinstance(data, dict) and ("id" in data or "status" in data)
    except:
        return False

def create_event(title, time_start, max_retries=3):
    composio_api_key = os.environ.get("COMPOSIO_API_KEY")
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}: Creating event '{title}' at {time_start}...")
        try:
            # Try native gog
            cmd = ["wsl", "--", "bash", "-c", f"gog calendar create --title='{title}' --time='{time_start}' --json"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if validate_creation(result.stdout):
                return json.loads(result.stdout)
        except Exception as e:
            print(f"gog tool failed on attempt {attempt}: {e}")
            
        # Try fallback
        try:
            if Composio:
                client = Composio(api_key=composio_api_key)
                res = client.tools.execute("GOOGLECALENDAR_CREATE_EVENT", arguments={"title": title, "start_time": time_start})
                if res.successful and validate_creation(res.data):
                    return res.data
        except Exception as e:
            print(f"Fallback composio failed on attempt {attempt}: {e}")
            
        print("Validation failed or tools errored. Retrying...")
        time.sleep(2)
        
    raise Exception("Failed to achieve expected outcome after max retries.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python node.py '<title>' '<start_time>'")
        sys.exit(1)
    title = sys.argv[1]
    time_start = sys.argv[2]
    print(json.dumps(create_event(title, time_start), indent=2))
