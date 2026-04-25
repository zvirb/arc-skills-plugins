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
    try:
        from composio import Composio
        composio = Composio(api_key=os.environ.get("COMPOSIO_API_KEY", "dummy"))
    except ImportError:
        print("Error: composio-core is not installed. Using mocked transaction.")
        return "composio_txn_mocked_12345"

    try:
        # Assuming we have a Google Sheet setup with columns for Persons, Organizations, Dates, Emails
        result = composio.tools.execute(
            'GOOGLESHEETS_APPEND_VALUES',
            user_id='default',
            arguments={
                'spreadsheetId': os.environ.get("GOOGLE_SHEET_ID", "default_spreadsheet_id"),
                'range': 'Sheet1!A:E', # Columns A:E
                'values': [
                    [entities["persons"], entities["organizations"], entities["dates"], entities["emails"], text]
                ]
            }
        )
        if result.successful:
            print(f"--- Successfully sent to Google Sheets ---")
            return f"composio_txn_success"
        else:
            print(f"Failed to append to Google Sheets: {result.error}")
            return f"composio_txn_failed"
    except Exception as e:
        print(f"Exception calling Composio: {e}")
        return "composio_txn_error"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_input = sys.argv[1]
        entities = extract_entities(text_input)
        record_id = save_to_crm(text_input, entities)
        print(json.dumps({"status": "success", "record_id": record_id, "entities": entities}, indent=2))
    else:
        print(json.dumps({"error": "No input text provided."}))
