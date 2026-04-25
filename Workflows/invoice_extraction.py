import os
import json
import importlib.util

def load_node(node_name):
    node_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Skills", node_name, "node.py"))
    spec = importlib.util.spec_from_file_location(f"{node_name}_node", node_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.execute_node

def run_invoice_workflow(query="invoice", sheet_id="default_sheet"):
    print("Workflow: Starting Invoice Extraction...")
    
    # Principle: Kaizen (改善) - decomposing the multi-service flow into atomic node edges
    search_node = load_node("Gmail-Search-Emails")
    retrieve_node = load_node("Gmail-Retrieve-Email")
    llm_json_node = load_node("LLM-Extract-JSON")
    append_node = load_node("Google-Sheets-Append-Row")

    # 1. Search Emails
    # Principle: Standardized Work (Hyojun Sagyo) - using efficient gog CLI before heavy SDKs
    print(f"Step 1: Searching for '{query}'...")
    search_args = json.dumps({"query": query})
    email_list = search_node(search_args)
    
    if not email_list:
        print("No emails found.")
        return []

    results = []
    # 2. Iterate through emails
    for email in email_list[:2]: # Limit to 2 for workflow safety
        email_id = email.get("id") or email.get("threadId")
        print(f"Step 2: Retrieving email {email_id}...")
        
        try:
            content = retrieve_node(json.dumps({"id": email_id}))
            body = content.get("body", str(content))
            
            print(f"Step 3: Extracting JSON via LLM (Gemma4/OpenClaw)...")
            llm_args = json.dumps({
                "text": body,
                "schema": "{'vendor': 'string', 'amount': 'number', 'date': 'string'}"
            })
            invoice_data = llm_json_node(llm_args)
            print(f"Extracted: {invoice_data}")
            
            print(f"Step 4: Appending to Sheets...")
            append_args = json.dumps({
                "spreadsheetId": sheet_id,
                "values": [[invoice_data.get("vendor"), invoice_data.get("amount"), invoice_data.get("date")]]
            })
            append_node(append_args)
            results.append(invoice_data)
        except Exception as e:
            # Principle: Jidoka (自働化) - stop immediately on detected defects
            print(f"Defect detected in invoice processing for email {email_id}: {e}")
            raise e
            
    print("Workflow Complete.")
    return results

if __name__ == "__main__":
    run_invoice_workflow()
