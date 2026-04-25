import sys
import os
import unittest
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/CRM-Entity-Extraction')))
import extractor

class TestCRMEntityExtraction(unittest.TestCase):
    def setUp(self):
        self.test_db = os.path.join(os.path.dirname(__file__), 'test_crm.db')
        extractor.DB_PATH = self.test_db

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_extract_and_save(self):
        text = "Meeting with John from Acme Inc on Oct 25, 2026. Contact john.doe@example.com."
        entities = extractor.extract_entities(text)
        
        self.assertIn("john.doe@example.com", entities["emails"])
        self.assertIn("Oct 25, 2026", entities["dates"])
        self.assertIn("Acme Inc", entities["organizations"])
        
        # Test DB insertion
        record_id = extractor.save_to_crm(text, entities)
        self.assertIsNotNone(record_id)
        
        conn = sqlite3.connect(extractor.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT persons, emails FROM interactions WHERE id=?", (record_id,))
        row = cursor.fetchone()
        self.assertEqual(row[0], "John Doe")
        self.assertIn("john.doe@example.com", row[1])
        conn.close()

if __name__ == '__main__':
    unittest.main()
