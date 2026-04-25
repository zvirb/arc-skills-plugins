import sys
import os
import unittest
import importlib.util
from unittest.mock import patch, MagicMock

def load_node_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

find_event_node = load_node_module('find_event_node', os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/Google-Calendar-Find-Event/node.py')))
create_event_node = load_node_module('create_event_node', os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/Google-Calendar-Create-Event/node.py')))

class TestAtomicNodes(unittest.TestCase):
    
    @patch.object(find_event_node.subprocess, 'run')
    def test_find_event_validation_loop(self, mock_subprocess):
        # First call fails validation (returns non-list string), second succeeds
        mock_subprocess.side_effect = [
            MagicMock(stdout='{"error": "not a list"}', returncode=0),
            MagicMock(stdout='[{"id": "event_123", "summary": "Meeting"}]', returncode=0)
        ]
        
        # We also need to mock time.sleep to avoid waiting 2 seconds
        with patch.object(find_event_node.time, 'sleep', return_value=None):
            result = find_event_node.find_event("meeting")
            
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "event_123")
        self.assertEqual(mock_subprocess.call_count, 2)

    @patch.object(create_event_node.subprocess, 'run')
    def test_create_event_validation_loop(self, mock_subprocess):
        # First call fails, second succeeds
        mock_subprocess.side_effect = [
            MagicMock(stdout='bad json', returncode=0),
            MagicMock(stdout='{"id": "new_event_abc", "status": "confirmed"}', returncode=0)
        ]
        
        with patch.object(create_event_node.time, 'sleep', return_value=None):
            result = create_event_node.create_event("Sync", "2026-05-01T10:00:00Z")
            
        self.assertEqual(result["id"], "new_event_abc")
        self.assertEqual(mock_subprocess.call_count, 2)

if __name__ == '__main__':
    unittest.main()
