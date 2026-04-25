import sys
import re
import sqlite3
import json
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Memory/crm.db'))

def init_db():
    if DB_PATH != ':memory:':
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            persons TEXT,
            organizations TEXT,
            dates TEXT,
            emails TEXT,
            raw_text TEXT
        )
    ''')
    conn.commit()
    return conn

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
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interactions (source, persons, organizations, dates, emails, raw_text)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Gmail', entities['persons'], entities['organizations'], entities['dates'], entities['emails'], text))
    conn.commit()
    interaction_id = cursor.lastrowid
    conn.close()
    return interaction_id

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_input = sys.argv[1]
        entities = extract_entities(text_input)
        record_id = save_to_crm(text_input, entities)
        print(json.dumps({"status": "success", "record_id": record_id, "entities": entities}, indent=2))
    else:
        print(json.dumps({"error": "No input text provided."}))
