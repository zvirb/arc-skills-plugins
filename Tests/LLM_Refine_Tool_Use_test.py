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

refine_tool_use_node = load_node_module('refine_tool_use_node', os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/LLM-Refine-Tool-Use/node.py')))

class TestLLMRefineToolUse(unittest.TestCase):
    
    @patch.object(refine_tool_use_node.subprocess, 'run')
    def test_refine_tool_use_validation_loop(self, mock_subprocess):
        # First call fails validation (returns non-dict string), second succeeds
        mock_subprocess.side_effect = [
            MagicMock(stdout='{"error": "not a valid dictionary"}', returncode=0),
            MagicMock(stdout='{"refined_strategy": "Use grep_search instead of grep.", "recommended_tools": ["grep_search"], "anti_patterns_to_avoid": ["grep in bash"]}', returncode=0)
        ]
        
        # Mock time.sleep to avoid waiting during tests
        with patch.object(refine_tool_use_node.time, 'sleep', return_value=None):
            result = refine_tool_use_node.refine_tool_use("Find instances of MockKException in the codebase.")
            
        self.assertIn("refined_strategy", result)
        self.assertIn("recommended_tools", result)
        self.assertIn("anti_patterns_to_avoid", result)
        self.assertEqual(result["recommended_tools"], ["grep_search"])
        self.assertEqual(mock_subprocess.call_count, 2)

if __name__ == '__main__':
    unittest.main()
