import os
import json
import importlib.util

def load_node(node_name):
    node_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Skills", node_name, "node.py"))
    spec = importlib.util.spec_from_file_location(f"{node_name}_node", node_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.execute_node

def run_vague_task_decomposition(vague_task):
    print(f"Workflow: Starting Vague Task Decomposition for: '{vague_task}'")
    
    # Principle: Kaizen (改善) - breaking the process into its simplest atomic components
    extraction_node = load_node("LLM-Extract-Action-Items")
    create_task_node = load_node("Google-Tasks-Create-Task")

    # 1. Extract Action Items
    # Principle: Standardized Work (Hyojun Sagyo) - most efficient path for decomposition
    print("Step 1: Decomposing task into actionable subtasks via LLM...")
    extraction_args = json.dumps({
        "text": vague_task,
        "schema": "A JSON array of strings, where each string is a clear, actionable subtask starting with a verb."
    })
    subtasks = extraction_node(extraction_args)
    
    if not subtasks:
        print("No subtasks extracted.")
        return []

    print(f"Decomposed into {len(subtasks)} subtasks: {subtasks}")

    results = []
    # 2. Create tasks in Google Tasks
    for task_title in subtasks:
        print(f"Step 2: Creating Google Task: '{task_title}'...")
        try:
            create_args = json.dumps({"title": task_title})
            res = create_task_node(create_args)
            results.append(res)
        except Exception as e:
            # Principle: Jidoka (自働化) - autonomous defect detection and halting
            print(f"Defect detected in creation step for '{task_title}': {e}")
            raise e
            
    print("Workflow Complete.")
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_vague_task_decomposition(sys.argv[1])
    else:
        print("Usage: python vague_task_decomposition.py '<vague_task_description>'")
