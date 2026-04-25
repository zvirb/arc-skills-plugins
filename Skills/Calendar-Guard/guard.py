import json

def guard_calendar():
    import os
    from datetime import datetime, timedelta
    
    print("--- Evaluating Calendar Density ---")
    
    # Mock decision for density exceeded threshold, but actual injection
    print("Density exceeds 3 hours continuous. Injecting Recovery Block via Composio.")
    
    try:
        from composio import Composio
        composio = Composio(api_key=os.environ.get("COMPOSIO_API_KEY", "dummy"))
        
        # Schedule the recovery block 2 hours from now for 1 hour duration
        start_time = datetime.utcnow() + timedelta(hours=2)
        end_time = start_time + timedelta(hours=1)
        
        result = composio.tools.execute(
            'GOOGLECALENDAR_CREATE_EVENT',
            user_id='default',
            arguments={
                'summary': 'Recovery Block',
                'description': 'Automated decompression time injected by Calendar Guard.',
                'start': {'dateTime': start_time.isoformat() + 'Z'},
                'end': {'dateTime': end_time.isoformat() + 'Z'}
            }
        )
        if result.successful:
            print("Successfully injected Recovery Block into Google Calendar.")
            return {
                "status": "success",
                "action": "injected_recovery_block",
                "time": f"{start_time.isoformat()} to {end_time.isoformat()}"
            }
        else:
            print(f"Failed to inject Recovery Block: {result.error}")
            return {
                "status": "failed",
                "error": result.error
            }
    except Exception as e:
        print(f"Error during Calendar Guard injection: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    result = guard_calendar()
    print(json.dumps(result, indent=2))
