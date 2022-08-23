from context import actions

from pathlib import Path

import unittest

class DataMungingCase(unittest.TestCase):

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
            
    def test_iterate_factbook_files(self):
        print('\n')
        for event in actions.readers.iterate_factbook_files(first_year=2005, last_year=2007):
            print(event.factbook, '-', event.root, '-', event.filename, ':', event.mimetype)
            

if __name__ == '__main__':
    unittest.main(verbosity=2)
