import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import unittest
from unittest.mock import patch
from micro_update_manager.process_manager import restart_processes


class TestProcessManager(unittest.TestCase):

    @patch('micro_update_manager.process_manager.subprocess.run')
    @patch('micro_update_manager.process_manager.can_restart_process')
    def test_restart_process_http_interface(self, mock_can_restart_process, mock_subprocess_run):
        # Setup mock to return True, meaning process can be restarted
        mock_can_restart_process.return_value = True

        config = {
            'processes': {
                'example_process': {
                    'interface': {
                        'type': 'http',
                        'host': 'localhost',
                        'port': 5000,
                        'endpoint': '/can_restart'
                    },
                    'command': 'python /path/to/your/script.py',
                    'params': '--arg1 value1'
                }
            }
        }
        process_list = ['example_process']

        # Run the function
        restart_processes(process_list, config)

        # Check that the HTTP check was called
        mock_can_restart_process.assert_called_once_with(config['processes']['example_process']['interface'], 'example_process')

        # Check that the subprocess.run was called to restart the process
        mock_subprocess_run.assert_called_once_with('python /path/to/your/script.py --arg1 value1', shell=True)

    @patch('micro_update_manager.process_manager.subprocess.run')
    @patch('micro_update_manager.process_manager.can_restart_process')
    def test_restart_process_http_interface_cannot_restart(self, mock_can_restart_process, mock_subprocess_run):
        # Setup mock to return False, meaning process cannot be restarted
        mock_can_restart_process.return_value = False

        config = {
            'processes': {
                'example_process': {
                    'interface': {
                        'type': 'http',
                        'host': 'localhost',
                        'port': 5000,
                        'endpoint': '/can_restart'
                    },
                    'command': 'python /path/to/your/script.py',
                    'params': '--arg1 value1'
                }
            }
        }
        process_list = ['example_process']

        # Run the function
        restart_processes(process_list, config)

        # Check that the HTTP check was called
        mock_can_restart_process.assert_called_once_with(config['processes']['example_process']['interface'], 'example_process')

        # Check that subprocess.run was not called since the process shouldn't restart
        mock_subprocess_run.assert_not_called()

    @patch('micro_update_manager.process_manager.can_restart_process')
    def test_restart_process_missing_config(self, mock_can_restart_process):
        # Ensure nothing is called if process is not in config
        config = {
            'processes': {
                'other_process': {
                    'interface': {
                        'type': 'http',
                        'host': 'localhost',
                        'port': 5000,
                        'endpoint': '/can_restart'
                    },
                    'command': 'python /path/to/your/script.py',
                    'params': '--arg1 value1'
                }
            }
        }
        process_list = ['example_process']

        with patch('builtins.print') as mock_print:
            restart_processes(process_list, config)

            # Check that the process is reported as missing in the config
            mock_print.assert_any_call("Process 'example_process' not found in the configuration.")

            # Ensure no HTTP request was made since the process config was missing
            mock_can_restart_process.assert_not_called()


if __name__ == '__main__':
    unittest.main()
