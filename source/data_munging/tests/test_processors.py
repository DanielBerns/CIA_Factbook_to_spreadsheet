from context import actions

from pathlib import Path

import unittest


class ActionsTestCase(unittest.TestCase):
        
    def test_filters(self):
        a_filter = actions.processors.FactbookFilter(
            factbook=lambda source: source == "factbook-2000",
            label=lambda source: source == 'fields',
            gate=actions.processors.or_fn)
        events_counter = actions.processors.EventCounterProcessor()
        for event in actions.processors.filter_factbook_events(a_filter):
            events_counter.update(event)
        with actions.processors.write_file(
            'test', 'alpha', 'processors-test_filters', 'events_counter.md', directory=actions.config.Config.APPLICATION_REPORTS) as target:
            events_counter.report(target)

if __name__ == '__main__':
    unittest.main(verbosity=2)
 
