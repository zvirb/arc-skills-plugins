import sys
import os
import unittest
import json
import importlib.util
from unittest.mock import patch, MagicMock

def load_node_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

refine_tool_use_node = load_node_module('refine_tool_use_node', os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/LLM-Refine-Tool-Use/node.py')))

class TestLLMRefineToolUse(unittest.TestCase):

    def setUp(self):
        # Ensure we have a clean history file for tests or use a temp file
        if os.path.exists(refine_tool_use_node.HISTORY_FILE):
            os.remove(refine_tool_use_node.HISTORY_FILE)

    def tearDown(self):
        if os.path.exists(refine_tool_use_node.HISTORY_FILE):
            os.remove(refine_tool_use_node.HISTORY_FILE)

    @patch.object(refine_tool_use_node.subprocess, 'run')
    def test_plan_action_validation_loop(self, mock_subprocess):
        # First call fails validation (returns non-dict string), second succeeds
        mock_subprocess.side_effect = [
            MagicMock(stdout='{"error": "not a valid dictionary"}', returncode=0),
            MagicMock(stdout='{"refined_strategy": "Use grep_search.", "recommended_tools": ["grep_search"], "anti_patterns_to_avoid": ["grep in bash"], "argument_constraints": {"grep_search": "Needs Query and SearchPath"}}', returncode=0)
        ]
        
        # Mock time.sleep to avoid waiting during tests
        with patch.object(refine_tool_use_node.time, 'sleep', return_value=None):
            result = refine_tool_use_node.refine_tool_use(json.dumps({
                "action": "plan",
                "task_description": "Find instances of MockKException in the codebase."
            }))
            
        self.assertIn("refined_strategy", result)
        self.assertIn("recommended_tools", result)
        self.assertIn("anti_patterns_to_avoid", result)
        self.assertIn("argument_constraints", result)
        self.assertEqual(result["recommended_tools"], ["grep_search"])
        self.assertEqual(mock_subprocess.call_count, 2)
        
    def test_record_action_updates_ledger(self):
        result = refine_tool_use_node.refine_tool_use(json.dumps({
            "action": "record",
            "use_case": "kotlin_debugging",
            "successful_tools": ["gradle_test_runner"],
            "anti_patterns": ["manual javac"],
            "notes": "Always use gradle to test kotlin.",
            "tool_name": "gradle_test_runner",
            "error_encountered": "Task not found error due to missing :app prefix",
            "argument_rule": "Always prefix gradle tasks with :app module"
        }))
        
        self.assertEqual(result["status"], "success")
        
        # Verify the file was created and contains the data
        history = refine_tool_use_node.load_history()
        self.assertIn("kotlin_debugging", history["use_cases"])
        self.assertIn("gradle_test_runner", history["use_cases"]["kotlin_debugging"]["successful_tools"])
        self.assertIn("manual javac", history["use_cases"]["kotlin_debugging"]["anti_patterns"])
        
        self.assertIn("gradle_test_runner", history["tool_constraints"])
        self.assertIn("Always prefix gradle tasks with :app module", history["tool_constraints"]["gradle_test_runner"]["argument_rules"])
        self.assertIn("Task not found error due to missing :app prefix", history["tool_constraints"]["gradle_test_runner"]["known_errors"])

if __name__ == '__main__':
    unittest.main()
