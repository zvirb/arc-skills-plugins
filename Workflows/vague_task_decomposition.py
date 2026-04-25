import os
import json
import importlib.util
import sys

# ==========================================
# STANDARDIZED WORK: NODE RUNNER UTILITY
# ==========================================
def run_node(node_name, arguments):
    """
    Standardized path to execute a Skill node.
    """
    node_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Skills", node_name, "node.py"))
    
    if not os.path.exists(node_path):
        return {"status": "error", "message": f"Node {node_name} not found at {node_path}"}
        
    try:
        spec = importlib.util.spec_from_file_location(f"{node_name}_node", node_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Every node now strictly takes a JSON string
        result = module.execute_node(json.dumps(arguments))
        return result
    except Exception as e:
        return {"status": "error", "message": f"Execution of {node_name} failed: {str(e)}"}

# ==========================================
# JIDOKA: WORKFLOW EXECUTION (ATOMIC STEPS)
# ==========================================
def run_vague_task_decomposition(vague_task):
    print(f"--- Starting Lean Vague Task Decomposition Workflow ---")
    
    # Step 1: Atomic Extraction
    print("[Step 1/2] Decomposing into subtasks...")
    extraction_args = {
        "text": vague_task,
        "schema": "A JSON array of strings, where each string is a clear, actionable subtask starting with a verb."
    }
    
    subtasks = run_node("LLM-Extract-Action-Items", extraction_args)
    
    # Jidoka: Stop if defect detected
    if isinstance(subtasks, dict) and subtasks.get("status") == "error":
        print(f"!!! Jidoka Stop: Extraction Failed: {subtasks.get('message')}")
        return subtasks
        
    if not isinstance(subtasks, list) or len(subtasks) == 0:
        print("!!! Jidoka Stop: Extraction Failed: No subtasks were returned.")
        return {"status": "error", "message": "No subtasks extracted."}

    print(f"Decomposed into {len(subtasks)} subtasks: {subtasks}")

    results = []
    # Step 2: Atomic Task Creation
    print("[Step 2/2] Creating Tasks...")
    for task_title in subtasks:
        print(f" -> Creating Google Task: '{task_title}'...")
        create_args = {"title": task_title}
        
        res = run_node("Google-Tasks-Create-Task", create_args)
        
        # Jidoka: Validation on individual subtask
        if isinstance(res, dict) and res.get("status") == "error":
            print(f"!!! Jidoka Defect: Task Creation Failed for '{task_title}': {res.get('message')}")
            # Depending on policy, we might continue or fail entirely.
            # Lean Jidoka means stopping the line to fix the defect.
            return {"status": "error", "message": f"Creation failed for task: {task_title}", "details": res}
            
        results.append(res)
            
    print("--- Workflow Success ---")
    return {"status": "success", "tasks_created": len(results), "data": results}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = run_vague_task_decomposition(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python vague_task_decomposition.py '<vague_task_description>'")
