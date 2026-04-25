import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/Vague-Task-Decomposition')))
import decompose

class TestVagueTaskDecomposition(unittest.TestCase):
    def test_decompose_task(self):
        vague_task = "Complete the TPS report"
        subtasks = decompose.decompose_task(vague_task)
        self.assertEqual(len(subtasks), 3)
        self.assertIn("Draft implementation plan", subtasks)

    def test_push_to_google_tasks(self):
        subtasks = ["Task 1", "Task 2"]
        results = decompose.push_to_google_tasks(subtasks)
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].startswith("Created Google Task"))

if __name__ == '__main__':
    unittest.main()
