from context import actions
from pathlib import Path

import unittest


class HelpersTestCase(unittest.TestCase):
        
    def test_get_timestamp(self):
        print('\n')
        timestamp = actions.helpers.get_timestamp()
        assert timestamp and len(timestamp) > 2
        
    def test_get_directory(self):
        print('\n')
        path = Path('./').resolve()
        directory = actions.helpers.get_directory(path)
        print('verify id', id(directory), id(path))

    def test_default_data_directory(self):
        directory = actions.helpers.default_data_directory('test', 'alpha')
        assert directory.exists()

    def test_default_reports_directory(self):
        directory = actions.helpers.default_reports_directory('test', 'alpha')
        assert directory.exists()
        
    def test_get_args(self):
        args = actions.helpers.get_args(Path('./').resolve())
        assert args['dotenv_path']


if __name__ == '__main__':
    unittest.main(verbosity=2)
