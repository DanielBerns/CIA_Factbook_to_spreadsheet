#!/usr/bin/env python
# from datetime import datetime, timedelta
from pathlib import Path 
import unittest
from actions import substrings, processors, readers
from config import Config


class TestConfig(Config):
    TESTING = True


def print_text(text: str) -> str:
    print('start', text[:80])
    print('end', text[-80:])
    print('length', len(text))


class DataMungingCase(unittest.TestCase):
        
    def test_main(self):
        print('\n')
        substrings.api.main()
        processors.api.main()
        readers.api.main()

    def test_compare(self):
        a, b = 1, 2
        red = f"testing {a:d} color {b:d}"
        blue = f"testing nada color azul"
        collector = substrings.api.compare(red, blue)
        print('\n')
        for key, start, stop in substrings.api.show_collector(collector):
            print(start, stop, key)

    def test_read_aa_html(self):
        print('\n')
        aa_path = Path("~", "Data", "CIA", "factbook", "factbook_html_zip", "factbook-2000", "geos", "aa.html").expanduser()
        aa_text = readers.api.read_text_file(aa_path)
        print_text(aa_text)
        ac_path = Path("~", "Data", "CIA", "factbook", "factbook_html_zip", "factbook-2000", "geos", "aa.html").expanduser()
        ac_text = readers.api.read_text_file(ac_path)
        print_text(ac_text)    
        collector = substrings.api.compare(aa_text, ac_text)
        print('\n')
        for key, start, stop in substrings.api.show_collector(collector):
            print(start, stop, key)


if __name__ == '__main__':
    unittest.main(verbosity=2)
