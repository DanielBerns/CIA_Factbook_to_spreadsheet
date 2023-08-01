from context import actions

from collections import Counter, defaultdict

import unittest


class ScrapCase(unittest.TestCase):
        
    def test_event_counter(self):
        actions.logs.LOGS.info('test_event_counter start')
        stats = actions.processors.EventCounterProcessor()
        for event in actions.readers.iterate_factbook_events():
            stats.update(event)
        with actions.processors.create_report(
            'test', '01', 'event_counter', 'report_01.md') as target:
            stats.report(target)
        actions.logs.LOGS.info('test_event_counter stop')            

if __name__ == '__main__':
    unittest.main(verbosity=2)
