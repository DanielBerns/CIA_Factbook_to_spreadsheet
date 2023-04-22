from context import actions

from pathlib import Path

import unittest

class ReadersCase(unittest.TestCase):

    def setUp(self):
        actions.logs.LOGS.info('ReadersTestCase start')
        
    def tearDown(self):
        actions.logs.LOGS.info('ReadersTestCase stop')

    def test_slurp_text_file(self):
        print('\n')
        text_path = Path("~", "Data", 
                         "CIA", "factbook", "factbook_html_zip", 
                         "download.txt").expanduser()
        text = actions.readers.slurp_text_file(text_path)
        assert len(text) > 0
        
    def test_readlines_text_file(self):
        print('\n')
        text_path = Path("~", "Data", 
                         "CIA", "factbook", "factbook_html_zip", 
                         "download.txt").expanduser()
        assert all(len(line) for line in actions.readers.readlines_text_file(text_path))
            
    def test_iterate_factbook_events(self):
        print('\n')
        for event in actions.readers.iterate_factbook_events(first_year=2005, last_year=2007):
            print(event.factbook, '-', event.label, '-', event.filename, ':', event.mimetype)
            

if __name__ == '__main__':
    unittest.main(verbosity=2)
