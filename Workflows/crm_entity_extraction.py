import os
import json
import importlib.util

def load_node(node_name):
    node_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Skills", node_name, "node.py"))
    spec = importlib.util.spec_from_file_location(f"{node_name}_node", node_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.execute_node

def run_crm_workflow(email_text, sheet_id="crm_sheet_id"):
    print("Workflow: Starting CRM Entity Extraction...")
    
    llm_json_node = load_node("LLM-Extract-JSON")
    append_node = load_node("Google-Sheets-Append-Row")

    print(f"Step 1: Extracting CRM Entities via LLM (Gemma4/OpenClaw)...")
    try:
        llm_args = json.dumps({
            "text": email_text,
            "schema": "{'persons': 'string', 'organizations': 'string', 'dates': 'string', 'emails': 'string'}"
        })
        crm_data = llm_json_node(llm_args)
        print(f"Extracted: {crm_data}")
        
        print(f"Step 2: Appending to CRM Sheets...")
        append_args = json.dumps({
            "spreadsheetId": sheet_id,
            "values": [[
                crm_data.get("persons", ""), 
                crm_data.get("organizations", ""), 
                crm_data.get("dates", ""), 
                crm_data.get("emails", ""), 
                email_text
            ]]
        })
        append_node(append_args)
        
        print("Workflow Complete.")
        return crm_data
    except Exception as e:
        print(f"Failed to process CRM Extraction: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_crm_workflow(sys.argv[1])
    else:
        print("Usage: python crm_entity_extraction.py '<email_text>'")
