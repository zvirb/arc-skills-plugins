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
def run_crm_workflow(email_text, sheet_id="crm_sheet_id"):
    print(f"--- Starting Lean CRM Workflow ---")

    # Step 1: Atomic Extraction
    print("[Step 1/2] Extracting Entities...")
    extraction_args = {
        "text": email_text,
        "schema": "{'persons': 'string', 'organizations': 'string', 'dates': 'string', 'emails': 'string'}"
    }
    
    crm_data = run_node("LLM-Extract-JSON", extraction_args)
    
    # Jidoka: Stop if defect detected
    if isinstance(crm_data, dict) and crm_data.get("status") == "error":
        print(f"!!! Jidoka Stop: Extraction Failed: {crm_data.get('message')}")
        return crm_data

    # Step 2: Atomic Persistence
    print("[Step 2/2] Appending to Sheets...")
    append_args = {
        "spreadsheetId": sheet_id,
        "values": [[
            crm_data.get("persons", "N/A"),
            crm_data.get("organizations", "N/A"),
            crm_data.get("dates", "N/A"),
            crm_data.get("emails", "N/A"),
            email_text[:500] # Sanitize input length
        ]]
    }
    
    persistence_result = run_node("Google-Sheets-Append-Row", append_args)

    # Jidoka: Final Validation
    if isinstance(persistence_result, dict) and persistence_result.get("status") == "error":
        print(f"!!! Jidoka Stop: Persistence Failed: {persistence_result.get('message')}")
        return persistence_result

    print("--- Workflow Success ---")
    return {"status": "success", "data": crm_data, "persistence": persistence_result}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = run_crm_workflow(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python crm_entity_extraction.py '<email_text>'")
