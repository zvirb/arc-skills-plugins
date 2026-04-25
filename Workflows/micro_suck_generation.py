import os
import json
import importlib.util

def load_node(node_name):
    node_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Skills", node_name, "node.py"))
    spec = importlib.util.spec_from_file_location(f"{node_name}_node", node_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_micro_suck_generation_workflow():
    print("Workflow: Starting Micro-Suck Generation...")
    
    random_node_mod = load_node("LLM-Select-Random-Item")
    create_task_node_mod = load_node("Google-Tasks-Create-Task")

    # 1. Select random micro-suck task
    tasks = [
        "Clear the physical desktop",
        "Drink a glass of water",
        "Stand up and stretch for 2 minutes",
        "Organize one folder on your computer",
        "Delete 5 unnecessary emails"
    ]
    
    print("Step 1: Selecting random task via LLM...")
    try:
        random_args = json.dumps({"items": tasks})
        selection = random_node_mod.execute_node(random_args)
        selected_task = selection.get("selected")
        print(f"Selected: '{selected_task}'")
        
        # 2. Inject to Google Tasks
        print(f"Step 2: Injecting task to Google Tasks...")
        create_args = json.dumps({"title": f"[Micro-Suck] {selected_task}"})
        res = create_task_node_mod.execute_node(create_args)
        
        print("Workflow Complete.")
        return res
    except Exception as e:
        print(f"Failed to generate micro-suck: {e}")
        return None

if __name__ == "__main__":
    run_micro_suck_generation_workflow()
