from context import actions
from pathlib import Path

import unittest


class HelpersTestCase(unittest.TestCase):

    def setUp(self):
        actions.logs.LOGS.info('HelpersTestCase start')
        
    def tearDown(self):
        actions.logs.LOGS.info('HelpersTestCase stop')
        
    def test_get_timestamp(self):
        print('\n')
        timestamp = actions.helpers.get_timestamp()
        assert timestamp and len(timestamp) > 2
        
    def test_get_directory(self):
        print('\n')
        path = Path('./').resolve()
        directory = actions.helpers.get_directory(path)
        print('verify id', id(directory), id(path))

    def test_save_json(self):
        actions.logs.LOGS.info('HelpersTestCase.save_json')
        assert False
        
    def test_load_json(self):
        actions.logs.LOGS.info('HelpersTestCase.load_json')
        assert False


if __name__ == '__main__':
    unittest.main(verbosity=2)
