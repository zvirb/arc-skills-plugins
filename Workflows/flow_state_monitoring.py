import os
import json
import importlib.util

def load_node(node_name):
    node_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Skills", node_name, "node.py"))
    spec = importlib.util.spec_from_file_location(f"{node_name}_node", node_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_flow_state_monitoring_workflow(telemetry_data="Detected single application focus for > 45 minutes."):
    print("Workflow: Starting Flow State Monitoring...")
    
    analyze_node_mod = load_node("LLM-Analyze-Flow-State")
    create_event_node_mod = load_node("Google-Calendar-Create-Event")

    # 1. Analyze focus
    print("Step 1: Analyzing telemetry via LLM...")
    try:
        analyze_args = json.dumps({"telemetry": telemetry_data})
        analysis = analyze_node_mod.execute_node(analyze_args)
        
        if analysis.get("is_in_flow"):
            print(f"Flow state detected (Confidence: {analysis.get('confidence')})")
            
            # 2. Update status/calendar
            print("Step 2: Syncing status to Google Calendar...")
            from datetime import datetime, timedelta
            start_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            
            create_args = json.dumps({
                "title": "Busy - In Flow",
                "start_time": start_time
            })
            res = create_event_node_mod.execute_node(create_args)
            
            print("Workflow Complete.")
            return res
        else:
            print("No flow state detected.")
            return None
    except Exception as e:
        print(f"Failed to monitor flow state: {e}")
        return None

if __name__ == "__main__":
    run_flow_state_monitoring_workflow()
