import json

def guard_calendar():
    # Simulated Google Calendar API evaluation
    print("--- Evaluating Calendar Density ---")
    
    # Mock decision: density exceeded threshold
    print("Density exceeds 3 hours continuous. Injecting Recovery Block.")
    
    return {
        "status": "success",
        "action": "injected_recovery_block",
        "time": "14:00-15:00"
    }

if __name__ == "__main__":
    result = guard_calendar()
    print(json.dumps(result, indent=2))
