import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Workflows')))
import invoice_extraction

class TestInvoiceWorkflow(unittest.TestCase):

    @patch('invoice_extraction.load_node')
    def test_invoice_workflow_end_to_end(self, mock_load_node):
        # We mock the atomic nodes to test the WORKFLOW chain logic.
        mock_search = MagicMock(return_value=[{"id": "msg_123"}])
        mock_retrieve = MagicMock(return_value={"body": "Your receipt from AWS. Total: $45.00 on 2026-04-25."})
        
        # In a real environment, this would hit OpenClaw -> Ollama -> Gemma4
        mock_llm = MagicMock(return_value={"vendor": "AWS", "amount": 45.00, "date": "2026-04-25"})
        
        mock_append = MagicMock(return_value={"updates": {"updatedRows": 1}})

        def side_effect(node_name):
            if node_name == "Gmail-Search-Emails": return mock_search
            if node_name == "Gmail-Retrieve-Email": return mock_retrieve
            if node_name == "LLM-Extract-JSON": return mock_llm
            if node_name == "Google-Sheets-Append-Row": return mock_append

        mock_load_node.side_effect = side_effect

        print("\\n--- Testing Invoice Extraction Workflow ---")
        results = invoice_extraction.run_invoice_workflow(query="invoice", sheet_id="test_sheet")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["vendor"], "AWS")
        self.assertEqual(results[0]["amount"], 45.0)
        
        # Verify the chain actually called each node with the expected dependencies
        mock_search.assert_called_once()
        mock_retrieve.assert_called_once()
        mock_llm.assert_called_once()
        mock_append.assert_called_once()

if __name__ == '__main__':
    unittest.main()
