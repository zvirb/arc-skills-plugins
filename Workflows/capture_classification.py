import os
import json
import importlib.util

def load_node(node_name):
    node_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Skills", node_name, "node.py"))
    spec = importlib.util.spec_from_file_location(f"{node_name}_node", node_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_capture_classification_workflow(text):
    print(f"Workflow: Starting Capture Classification for: '{text}'")
    
    classify_node_mod = load_node("LLM-Classify-Intent")
    create_task_node_mod = load_node("Google-Tasks-Create-Task")
    upsert_memory_node_mod = load_node("Vector-Store-Upsert-Memory")

    # 1. Classify intent
    print("Step 1: Classifying intent via LLM...")
    try:
        classify_args = json.dumps({"text": text})
        classification = classify_node_mod.execute_node(classify_args)
        
        intent = classification.get("intent")
        urgency = classification.get("urgency")
        print(f"Intent: {intent}, Urgency: {urgency}")
        
        if intent == "actionable":
            # 2a. Route to Google Tasks
            print("Step 2: Routing to Google Tasks...")
            create_args = json.dumps({"title": text})
            res = create_task_node_mod.execute_node(create_args)
            print("Workflow Complete (Routed to Tasks).")
            return res
        else:
            # 2b. Route to Vector Store
            print("Step 2: Routing to Vector Store (LanceDB)...")
            upsert_args = json.dumps({"text": text, "metadata": classification})
            res = upsert_memory_node_mod.execute_node(upsert_args)
            print("Workflow Complete (Routed to Memory).")
            return res
    except Exception as e:
        print(f"Failed to process capture classification: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_capture_classification_workflow(sys.argv[1])
    else:
        print("Usage: python capture_classification.py '<capture_text>'")
