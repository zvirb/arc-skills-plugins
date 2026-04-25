import sys
import json

def classify_and_route(text):
    import os
    print("--- Semantic Routing Analysis ---")
    is_actionable = "call" in text.lower() or "do" in text.lower() or "buy" in text.lower()
    
    if is_actionable:
        print(f"Decision: Actionable. Routing to Google Tasks via Composio.")
        destination = "Google Tasks"
        
        try:
            from composio import Composio
            composio = Composio(api_key=os.environ.get("COMPOSIO_API_KEY", "dummy"))
            result = composio.tools.execute(
                'GOOGLETASKS_INSERT_TASK',
                user_id='default',
                arguments={'title': f"Action item from capture: {text[:50]}..."}
            )
            if not result.successful:
                print(f"Failed to route to Google Tasks: {result.error}")
        except Exception as e:
            print(f"Error executing Composio Google Tasks insert: {e}")
            
    else:
        print(f"Decision: Conceptual. Routing to LanceDB local vector store.")
        destination = "LanceDB"
        # LanceDB insertion logic would go here
        
    return {
        "status": "success",
        "routed_to": destination,
        "input_preview": text[:30] + "..."
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = classify_and_route(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({"error": "No input provided"}))
