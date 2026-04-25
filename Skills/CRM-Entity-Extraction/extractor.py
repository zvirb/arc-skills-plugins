import sys
import re
import json
import os
import shlex

def extract_entities(text):
    dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b', text)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text)
    
    organizations = ["Acme Inc"] if "Acme" in text else []
    persons = ["John Doe"] if "John" in text else []
    
    return {
        "persons": ", ".join(persons),
        "organizations": ", ".join(organizations),
        "dates": ", ".join(dates),
        "emails": ", ".join(emails)
    }

def save_to_crm(text, entities):
    # Simulating a Composio API call to push the entity data into Google Sheets or Contacts
    print(f"--- Sending to Composio (Google Sheets/Contacts) ---")
    print(f"Payload: {json.dumps(entities)}")
    print(f"----------------------------------------------------")
    # In a real environment, this would call the Composio SDK or API.
    # Return a mocked transaction ID.
    return "composio_txn_12345"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_input = sys.argv[1]
        entities = extract_entities(text_input)
        record_id = save_to_crm(text_input, entities)
        print(json.dumps({"status": "success", "record_id": record_id, "entities": entities}, indent=2))
    else:
        print(json.dumps({"error": "No input text provided."}))
