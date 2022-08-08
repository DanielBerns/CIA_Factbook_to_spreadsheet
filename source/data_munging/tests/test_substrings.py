from context import substrings
from pathlib import Path
import unittest

class TestSubStrings(unittest.TestCase):
        
    def test_main(self):
        print('\n')
        substrings.main()

    def test_compare(self):
        a, b = 1, 2
        red = f"testing {a:d} color {b:d}"
        blue = f"testing nada color azul"
        collector = substrings.compare(red, blue)
        print('\n')
        for key, start, stop in substrings.show_collector(collector):
            print(start, stop, key)

    def test_compare_html(self):
        redpath = Path("~/Data/CIA/factbook/factbook_html_zip/factbook-2000/geos/aa.html").expanduser()
        bluepath = Path("~/Data/CIA/factbook/factbook_html_zip/factbook-2000/geos/ac.html").expanduser()
        
        with open(redpath, 'r') as source:
            red = source.read()
        with open(bluepath, 'r') as source:
            blue = source.read()            
        collector = substrings.compare(red, blue)
        print('\n')
        for key, start, stop in substrings.show_collector(collector):
            print(start, stop, key)        

if __name__ == '__main__':
    unittest.main()

