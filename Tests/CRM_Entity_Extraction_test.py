import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/CRM-Entity-Extraction')))
import extractor

class TestCRMEntityExtraction(unittest.TestCase):
    def test_extract_entities(self):
        text = "Meeting with John from Acme Inc on Oct 25, 2026. Contact john.doe@example.com."
        entities = extractor.extract_entities(text)
        
        self.assertIn("john.doe@example.com", entities["emails"])
        self.assertIn("Oct 25, 2026", entities["dates"])
        self.assertIn("Acme Inc", entities["organizations"])
        self.assertIn("John Doe", entities["persons"])
        
    @patch('composio.Composio')
    def test_save_to_crm(self, mock_composio_class):
        # Mock the composio client and tools.execute
        mock_client = MagicMock()
        mock_composio_class.return_value = mock_client
        mock_result = MagicMock()
        mock_result.successful = True
        mock_client.tools.execute.return_value = mock_result
        
        text = "Meeting with John"
        entities = {"persons": "John Doe", "organizations": "Acme Inc", "dates": "Oct 25, 2026", "emails": "john@example.com"}
        
        record_id = extractor.save_to_crm(text, entities)
        self.assertEqual(record_id, "composio_txn_success")
        mock_client.tools.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
