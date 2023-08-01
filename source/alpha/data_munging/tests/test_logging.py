from context import actions

import unittest


class LoggingTestCase(unittest.TestCase):

    def setUp(self):
        actions.logs.LOGS.info('LoggingTestCase start')
        
    def tearDown(self):
        actions.logs.LOGS.info('LoggingTestCase stop')
        
    def test_logging(self):
        print('LOG_TO_STDOUT =', actions.config.Config.LOG_TO_STDOUT)
        actions.logs.LOGS.info('We are here at test_logging')


if __name__ == '__main__':
    unittest.main(verbosity=2)
