from context import actions

from pathlib import Path

import unittest

class DataMungingCase(unittest.TestCase):

    def test_slurp_text_file(self):
        print('\n')
        text_path = Path("~", 
                         "Data", "CIA", "factbook", "factbook_html_zip", "download.txt").expanduser()
        text = actions.readers.slurp_text_file(text_path)
        assert len(text) > 0
        
    def test_read_text_file(self):
        print('\n')
        text_path = Path("~", 
                         "Data", "CIA", "factbook", "factbook_html_zip", "download.txt").expanduser()
        assert all(len(line) for line in actions.readers.readlines_text_file(text_path))
            
    def test_read_root_and_file(self):
        print('\n')
        directory = Path("~", "Data", "CIA", "factbook", "factbook_html_zip").expanduser()
        for number, (root, a_file) in enumerate(actions.readers.read_root_and_file(directory)):
            print(number, '-', str(root), '-', a_file)
            
    def test_get_root_and_file_with_mimetypes(self):
        print('\n')
        directory = Path("~", "Data", "CIA", "factbook", "factbook_html_zip").expanduser()
        factbook_years = ["factbook-2000", "factbook-2001"]
        for root, a_file, mimetype in actions.readers.read_root_and_file_with_mimetype(directory):
            print('-', str(root), '-', a_file, ':', mimetype)


if __name__ == '__main__':
    unittest.main(verbosity=2)
