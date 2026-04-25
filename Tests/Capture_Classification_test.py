import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/Capture-Classification')))
import router

class TestCaptureClassification(unittest.TestCase):
    @patch('composio.Composio')
    def test_classify_actionable(self, mock_composio_class):
        mock_client = MagicMock()
        mock_composio_class.return_value = mock_client
        mock_result = MagicMock()
        mock_result.successful = True
        mock_client.tools.execute.return_value = mock_result
        
        result = router.classify_and_route("I need to call the supplier today")
        self.assertEqual(result["routed_to"], "Google Tasks")
        mock_client.tools.execute.assert_called_once()
        
    def test_classify_conceptual(self):
        result = router.classify_and_route("This is a cool idea for the project")
        self.assertEqual(result["routed_to"], "LanceDB")

if __name__ == '__main__':
    unittest.main()
