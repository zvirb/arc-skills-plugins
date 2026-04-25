import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Skills/Flow-State-Monitoring')))
import monitor

class TestFlowStateMonitoring(unittest.TestCase):
    @patch('composio.Composio')
    def test_monitor_flow(self, mock_composio_class):
        mock_client = MagicMock()
        mock_composio_class.return_value = mock_client
        mock_result = MagicMock()
        mock_result.successful = True
        mock_client.tools.execute.return_value = mock_result
        
        result = monitor.monitor_flow()
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["action"], "set_do_not_disturb")
        mock_client.tools.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
