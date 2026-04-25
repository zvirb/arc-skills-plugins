import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Workflows')))
import crm_entity_extraction

class TestCRMExtractionWorkflow(unittest.TestCase):

    @patch('crm_entity_extraction.load_node')
    def test_crm_workflow_end_to_end(self, mock_load_node):
        # In a real environment, this would hit OpenClaw -> Ollama -> Gemma4
        mock_llm = MagicMock(return_value={
            "persons": "John Doe", 
            "organizations": "Acme Inc", 
            "dates": "2026-04-25", 
            "emails": "john@acme.com"
        })
        
        mock_append = MagicMock(return_value={"updates": {"updatedRows": 1}})

        def side_effect(node_name):
            if node_name == "LLM-Extract-JSON": return mock_llm
            if node_name == "Google-Sheets-Append-Row": return mock_append

        mock_load_node.side_effect = side_effect

        print("\\n--- Testing CRM Extraction Workflow ---")
        input_text = "Hi, this is John Doe from Acme Inc. Let's meet on 2026-04-25. My email is john@acme.com."
        result = crm_entity_extraction.run_crm_workflow(email_text=input_text, sheet_id="test_crm_sheet")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["persons"], "John Doe")
        self.assertEqual(result["organizations"], "Acme Inc")
        
        # Verify the chain actually called each node with the expected dependencies
        mock_llm.assert_called_once()
        mock_append.assert_called_once()

if __name__ == '__main__':
    unittest.main()
