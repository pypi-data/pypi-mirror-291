import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import unittest
from micro_update_manager.config_loader import load_config


class TestConfigLoader(unittest.TestCase):
    def test_load_config(self):
        config = load_config('tests/example_config.yaml')
        self.assertIsInstance(config, dict)
        self.assertIn('packages', config)
        self.assertIn('processes', config)


if __name__ == '__main__':
    unittest.main()
