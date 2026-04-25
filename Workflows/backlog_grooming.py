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

def run_backlog_grooming_workflow():
    print("Workflow: Starting Backlog Grooming...")
    
    find_node_mod = load_node("Google-Tasks-Find-Tasks")
    update_node_mod = load_node("Google-Tasks-Update-Task")
    summarize_node_mod = load_node("LLM-Summarize-Text")

    # 1. Fetch active tasks
    print("Step 1: Fetching active tasks...")
    tasks = find_node_mod.execute_node(json.dumps({})) # Empty query for all active
    
    if not tasks:
        print("No active tasks found.")
        return []

    print(f"Retrieved {len(tasks)} tasks.")

    results = []
    # 2. Identify stale tasks and groom
    # Threshold: 30 days. gog usually returns 'updated' or 'created'
    now = datetime.now()
    
    for task in tasks:
        # Some crude logic to check age - in a real scenario we'd parse the date
        # For the workflow demo, we'll assume we groom any task with 'STALE' heuristic or just simulate
        updated_str = task.get("updated")
        is_stale = False
        if updated_str:
            try:
                # Basic ISO parse
                updated_dt = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
                if now - updated_dt.replace(tzinfo=None) > timedelta(days=30):
                    is_stale = True
            except:
                pass

        if is_stale:
            print(f"Grooming stale task: '{task.get('title')}'")
            
            # 3. Summarize and prepend
            try:
                sum_args = json.dumps({
                    "text": task.get("title") + " " + (task.get("notes") or ""),
                    "schema": "{'summary': 'string'}"
                })
                summary_data = summarize_node_mod.execute_node(sum_args)
                new_title = f"[STALE/ARCHIVED] {summary_data.get('summary')}"
                
                # 4. Update task
                update_args = json.dumps({
                    "id": task.get("id"),
                    "title": new_title,
                    "status": "completed" # Archive by completing
                })
                res = update_node_mod.execute_node(update_args)
                results.append(res)
            except Exception as e:
                print(f"Failed to groom task '{task.get('id')}': {e}")
                
    print("Workflow Complete.")
    return results

if __name__ == "__main__":
    run_backlog_grooming_workflow()
