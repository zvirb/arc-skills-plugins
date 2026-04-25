import sys
import json

def classify_and_route(text):
    # Simulated semantic routing logic
    print("--- Semantic Routing Analysis ---")
    is_actionable = "call" in text.lower() or "do" in text.lower() or "buy" in text.lower()
    
    if is_actionable:
        print(f"Decision: Actionable. Routing to Google Tasks via Composio.")
        destination = "Google Tasks"
    else:
        print(f"Decision: Conceptual. Routing to LanceDB local vector store.")
        destination = "LanceDB"
        
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
