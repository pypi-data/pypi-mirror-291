import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import unittest
import requests
from unittest.mock import patch, MagicMock
from micro_update_manager.interfaces.http_interface import can_restart_process


class TestHttpInterface(unittest.TestCase):

    @patch('micro_update_manager.interfaces.http_interface.requests.get')
    def test_can_restart_process_success(self, mock_get):
        # Simulate a successful HTTP GET request with 'can_restart' set to True
        mock_response = MagicMock()
        mock_response.json.return_value = {'can_restart': True}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        interface_config = {
            'host': 'localhost',
            'port': 5000,
            'endpoint': '/can_restart'
        }
        process_name = 'example_process'

        result = can_restart_process(interface_config, process_name)
        self.assertTrue(result)  # Should return True

    @patch('micro_update_manager.interfaces.http_interface.requests.get')
    def test_can_restart_process_no_restart(self, mock_get):
        # Simulate a successful HTTP GET request with 'can_restart' set to False
        mock_response = MagicMock()
        mock_response.json.return_value = {'can_restart': False}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        interface_config = {
            'host': 'localhost',
            'port': 5000,
            'endpoint': '/can_restart'
        }
        process_name = 'example_process'

        result = can_restart_process(interface_config, process_name)
        self.assertFalse(result)  # Should return False

    @patch('micro_update_manager.interfaces.http_interface.requests.get')
    def test_can_restart_process_http_error(self, mock_get):
        # Simulate an HTTP error (e.g., 404 Not Found)
        mock_get.side_effect = requests.HTTPError("404 Client Error: Not Found for url")

        interface_config = {
            'host': 'localhost',
            'port': 5000,
            'endpoint': '/can_restart'
        }
        process_name = 'example_process'

        result = can_restart_process(interface_config, process_name)
        self.assertFalse(result)  # Should return False due to HTTP error

    @patch('micro_update_manager.interfaces.http_interface.requests.get')
    def test_can_restart_process_connection_error(self, mock_get):
        # Simulate a connection error
        mock_get.side_effect = requests.ConnectionError("Failed to establish a new connection")

        interface_config = {
            'host': 'localhost',
            'port': 5000,
            'endpoint': '/can_restart'
        }
        process_name = 'example_process'

        result = can_restart_process(interface_config, process_name)
        self.assertFalse(result)  # Should return False due to connection error


if __name__ == '__main__':
    unittest.main()
