from context import actions

import unittest


class LoggingTestCase(unittest.TestCase):
        
    def test_logging(self):
        application = actions.config.APPLICATION
        version = actions.config.VERSION
        logger = actions.logs.start_logs(application, version, 'test/test_logging.py')
        logger.info('We are here at test_logging')


if __name__ == '__main__':
    unittest.main(verbosity=2)
