import json
import sys

def monitor_flow():
    # Simulated CatchMe telemetry
    print("--- Analyzing CatchMe Telemetry ---")
    print("Detected single application focus for > 45 minutes.")
    
    return {
        "status": "success",
        "action": "set_do_not_disturb",
        "google_workspace": "Busy - In Flow"
    }

if __name__ == "__main__":
    result = monitor_flow()
    print(json.dumps(result, indent=2))
