from context import actions

import unittest

import pdb

class LoggingTestCase(unittest.TestCase):
        
    def test_logging(self):
        print('LOG_TO_STDOUT =', actions.config.Config.LOG_TO_STDOUT)
        pdb.set_trace()
        actions.logs.start_logs('test', 'alpha')
        actions.logs.LOGS.info('We are here at test_logging')


if __name__ == '__main__':
    unittest.main(verbosity=2)
