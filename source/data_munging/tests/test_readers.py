from context import readers
from pathlib import Path
import unittest

class TestReaders(unittest.TestCase):
        
    def test_read_aa_html(self):
        print('\n')
        text_path = Path("~", "Data", "CIA", "factbook", "factbook_html_zip", "factbook-2000", "geos", "aa.html").expanduser()
        text = readers.read_text_file(text_path)
        print('start', text[:80])
        print('end', text[-80:])
        print('length', len(text))

#     bluepath = Path("~/Data/CIA/factbook/factbook_html_zip/factbook-2000/geos/ac.html").expanduser()

if __name__ == '__main__':
    unittest.main()

