import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/Backlog-Grooming')))
import groomer

class TestBacklogGrooming(unittest.TestCase):
    @patch('composio.Composio')
    def test_groom_tasks(self, mock_composio_class):
        mock_client = MagicMock()
        mock_composio_class.return_value = mock_client
        
        mock_list_result = MagicMock()
        mock_list_result.successful = True
        # Return one task from 2 months ago, one recent
        mock_list_result.data = {
            'items': [
                {"id": "1", "title": "Old Task", "updated": "2026-02-01T00:00:00Z"},
                {"id": "2", "title": "New Task", "updated": "2026-04-20T00:00:00Z"}
            ]
        }
        
        mock_patch_result = MagicMock()
        mock_patch_result.successful = True
        
        mock_client.tools.execute.side_effect = [mock_list_result, mock_patch_result]
        
        result = groomer.groom_tasks()
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["tasks_groomed"], 1)
        self.assertEqual(result["details"][0]["id"], "1")
        self.assertEqual(mock_client.tools.execute.call_count, 2)

if __name__ == '__main__':
    unittest.main()
