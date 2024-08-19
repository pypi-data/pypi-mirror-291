import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import unittest
from unittest.mock import patch
from micro_update_manager.package_updater import check_for_updates, monitor_packages


class TestPackageUpdater(unittest.TestCase):

    @patch('micro_update_manager.package_updater.get_outdated_packages')
    def test_check_for_updates_outdated(self, mock_get_outdated_packages):
        # Mock the get_outdated_packages to return that 'example' package is outdated
        mock_get_outdated_packages.return_value = {
            'example': ('1.0.0', '1.1.0')
        }

        package = {'name': 'example', 'requires_restart': False}
        result = check_for_updates(package)

        self.assertTrue(result)  # Should return True because an update is available

    @patch('micro_update_manager.package_updater.get_outdated_packages')
    def test_check_for_updates_no_update(self, mock_get_outdated_packages):
        # Mock the get_outdated_packages to return an empty dict (no outdated packages)
        mock_get_outdated_packages.return_value = {}

        package = {'name': 'example', 'requires_restart': False}
        result = check_for_updates(package)

        self.assertFalse(result)  # Should return False because no update is available

    @patch('micro_update_manager.package_updater.get_outdated_packages')
    @patch('micro_update_manager.package_updater.check_for_updates')
    def test_monitor_packages(self, mock_check_for_updates, mock_get_outdated_packages):
        # Mock get_outdated_packages to return that 'example' package is outdated
        mock_get_outdated_packages.return_value = {
            'example': ('1.0.0', '1.1.0')
        }
        mock_check_for_updates.return_value = True

        config = {
            'packages': [{'name': 'example', 'requires_restart': True}]
        }
        updated_packages = monitor_packages(config)

        self.assertEqual(len(updated_packages), 1)  # Expect 1 package that needs a restart
        self.assertEqual(updated_packages[0]['name'], 'example')

    # def test_real_check_for_updates(self):
    #     package = {'name': 'numpy', 'requires_restart': False}
    #     result = check_for_updates(package)

    #     # This is a real test against the current state of 'numpy' in the environment
    #     # May return True or False depending on if numpy is outdated or not
    #     # This test may not be consistent across different environments
    #     self.assertIsInstance(result, bool)


if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
