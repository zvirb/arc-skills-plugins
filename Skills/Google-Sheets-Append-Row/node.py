import sys
import json
import time
import subprocess
import os

# ==========================================
# STANDARDIZED WORK: CONFIGURATION
# ==========================================
MAX_RETRIES = 3
DEFAULT_RANGE = "Sheet1!A1"

try:
    from composio import Composio
except ImportError:
    Composio = None

# Add parent directory to sys.path to import Shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from Shared.utils import evaluate_tool_output

# ==========================================
# EXECUTION LOGIC (ATOMIC)
# ==========================================
def execute_node(arguments_json_str):
    # 1. Standardized Input Parsing
    try:
        args = json.loads(arguments_json_str)
    except:
        return {"status": "error", "message": "Invalid JSON input."}

    spreadsheet_id = args.get("spreadsheetId") or args.get("spreadsheet_id")
    values = args.get("values", [])
    
    if not spreadsheet_id:
        return {"status": "error", "message": "Missing spreadsheetId."}

    last_error = ""

    # 2. Jidoka: The "Andon" Loop (Self-Healing)
    for attempt in range(1, MAX_RETRIES + 1):
        # Path A: Native 'gog' execution (Efficient)
        try:
            # Atomic tool execution
            cmd = ["wsl", "--", "bash", "-c", f"gog sheets append --spreadsheetId='{spreadsheet_id}' --values='{json.dumps(values)}' --json"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                is_valid, data = evaluate_tool_output(json.loads(result.stdout), "gog")
                if is_valid: return data
                last_error = data
            else:
                last_error = result.stderr or "Unknown shell error."
                
        except Exception as e:
            last_error = str(e)

        # Path B: Composio Fallback
        if Composio and os.environ.get("COMPOSIO_API_KEY"):
            try:
                client = Composio()
                res = client.tools.execute("GOOGLESHEETS_APPEND_VALUES", arguments=args)
                if res.successful:
                    is_valid, data = evaluate_tool_output(res.data, "Composio")
                    if is_valid: return data
                    last_error = data
                else:
                    last_error = res.error or "Composio execution failed."
            except Exception as e:
                last_error = f"Composio Exception: {str(e)}"

        time.sleep(1)

    # 3. Deterministic Exit
    return {
        "status": "error",
        "message": f"Failed to append to sheet after {MAX_RETRIES} attempts.",
        "last_error": last_error,
        "spreadsheet_id": spreadsheet_id
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Missing arguments."}))
        sys.exit(1)
    
    print(json.dumps(execute_node(sys.argv[1]), indent=2))
