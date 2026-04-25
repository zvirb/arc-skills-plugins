import json
import sys

def monitor_flow():
    import os
    from datetime import datetime, timedelta
    
    # Simulated CatchMe telemetry
    print("--- Analyzing CatchMe Telemetry ---")
    print("Detected single application focus for > 45 minutes.")
    
    try:
        from composio import Composio
        composio = Composio(api_key=os.environ.get("COMPOSIO_API_KEY", "dummy"))
        
        # Inject "Busy - In Flow" event for the next hour to block schedule and show as busy
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(hours=1)
        
        result = composio.tools.execute(
            'GOOGLECALENDAR_CREATE_EVENT',
            user_id='default',
            arguments={
                'summary': 'Busy - In Flow',
                'description': 'Automatically set by Flow State Monitor.',
                'start': {'dateTime': start_time.isoformat() + 'Z'},
                'end': {'dateTime': end_time.isoformat() + 'Z'}
            }
        )
        if result.successful:
            return {
                "status": "success",
                "action": "set_do_not_disturb",
                "google_workspace": "Busy - In Flow (Event Created)"
            }
        else:
            return {
                "status": "failed",
                "error": result.error
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    result = monitor_flow()
    print(json.dumps(result, indent=2))
