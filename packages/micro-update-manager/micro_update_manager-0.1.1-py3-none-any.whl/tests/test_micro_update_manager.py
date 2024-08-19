import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import unittest
from unittest.mock import patch
from micro_update_manager.micro_update_manager import main


class TestMainApplication(unittest.TestCase):

    @patch('micro_update_manager.micro_update_manager.restart_processes')
    @patch('micro_update_manager.micro_update_manager.monitor_packages')
    @patch('micro_update_manager.micro_update_manager.load_config')
    def test_main_loop_single_iteration(self, mock_load_config, mock_monitor_packages, mock_restart_processes):
        # Set up mock configuration and behavior
        mock_load_config.return_value = {
            'refresh_interval': 1,  # Set to 1 second for testing
            'packages': [{'name': 'example', 'requires_restart': True, 'processes_to_restart': ['process1']}]
        }
        mock_monitor_packages.return_value = [{'name': 'example', 'requires_restart': True, 'processes_to_restart': ['process1']}]

        mock_restart_processes.side_effect = SystemExit
        # Mock the infinite loop control to exit after one iteration
        with self.assertRaises(SystemExit):  # Expect SystemExit to be raised
            main()

#        mock_load_config.assert_called_once_with('config.yaml')
#        mock_monitor_packages.assert_called_once_with(mock_load_config.return_value)
#        mock_restart_processes.assert_called_once_with(['process1'], mock_load_config.return_value)


if __name__ == '__main__':
    unittest.main()
