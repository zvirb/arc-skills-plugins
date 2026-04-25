import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/Google-Workspace-Orchestrator')))
import workspace_manager

class TestGoogleWorkspaceOrchestrator(unittest.TestCase):
    @patch('workspace_manager.WorkspaceManager.run_gog')
    def test_search_emails(self, mock_run_gog):
        mock_run_gog.return_value = [{"id": "123", "snippet": "Test email snippet"}]
        
        manager = workspace_manager.WorkspaceManager()
        results = manager.search_emails("test query")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "123")
        mock_run_gog.assert_called_with(["gmail", "search", "'test query'"])

    @patch('workspace_manager.WorkspaceManager.run_gog')
    def test_schedule_task(self, mock_run_gog):
        # First call: calendar list, Second call: calendar create
        mock_run_gog.side_effect = [[], {"status": "created", "id": "event_456"}]
        
        manager = workspace_manager.WorkspaceManager()
        result = manager.schedule_task("Analyze metrics", 30, "2026-05-01")
        
        self.assertEqual(result["status"], "created")
        self.assertEqual(mock_run_gog.call_count, 2)

if __name__ == '__main__':
    unittest.main()
