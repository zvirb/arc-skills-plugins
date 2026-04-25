import os
import json
import importlib.util
from datetime import datetime, timedelta

def load_node(node_name):
    node_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Skills", node_name, "node.py"))
    spec = importlib.util.spec_from_file_location(f"{node_name}_node", node_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_calendar_guard_workflow():
    print("Workflow: Starting Calendar Guard...")
    
    find_node_mod = load_node("Google-Calendar-Find-Event")
    create_node_mod = load_node("Google-Calendar-Create-Event")
    conflict_node_mod = load_node("LLM-Identify-Conflicts")

    # 1. Fetch upcoming events (next 24 hours)
    print("Step 1: Fetching upcoming calendar events...")
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    
    # query string for gog/composio
    query = f"after:{now.strftime('%Y-%m-%dT%H:%M:%SZ')} before:{tomorrow.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    events = find_node_mod.find_event(query)
    
    if not events:
        print("No events found for the next 24 hours.")
        return []

    print(f"Retrieved {len(events)} events.")

    # 2. Identify density/conflicts via LLM
    print("Step 2: Analyzing schedule density via LLM...")
    conflict_args = json.dumps({
        "text": json.dumps(events),
        "schema": "A JSON array of 'Recovery Block' objects with 'title' and 'start_time' if a block of meetings exceeds 3 hours."
    })
    recovery_blocks = conflict_node_mod.execute_node(conflict_args)

    if not recovery_blocks:
        print("Schedule is healthy. No recovery blocks needed.")
        return []

    print(f"LLM identified {len(recovery_blocks)} required recovery blocks.")

    results = []
    # 3. Inject Recovery Blocks
    for block in recovery_blocks:
        title = block.get("title", "Recovery Block")
        start_time = block.get("start_time")
        print(f"Step 3: Injecting {title} at {start_time}...")
        try:
            res = create_node_mod.create_event(title, start_time)
            results.append(res)
        except Exception as e:
            print(f"Failed to inject recovery block: {e}")
            
    print("Workflow Complete.")
    return results

if __name__ == "__main__":
    run_calendar_guard_workflow()
