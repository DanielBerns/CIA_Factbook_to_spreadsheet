from context import actions

from pathlib import Path

import unittest


class SubstringsTestCase(unittest.TestCase):
        
    def test_compare_text(self):
        a, b = 1, 2
        red = f"testing {a:d} color {b:d}"
        blue = f"testing nada color azul"
        collector = actions.substrings.compare(red, blue)
        print('\n')
        for key, start, stop in actions.substrings.common_substrings(collector):
            print(start, stop, key)

    def test_compare_html(self):
        print('\n')
        aa_path = Path("~", "Data", "CIA", "factbook", "factbook_html_zip", "factbook-2000", "geos", "aa.html").expanduser()
        aa_text = actions.readers.slurp_text_file(aa_path)
        ac_path = Path("~", "Data", "CIA", "factbook", "factbook_html_zip", "factbook-2000", "geos", "aa.html").expanduser()
        ac_text = actions.readers.slurp_text_file(ac_path)
        collector = actions.substrings.compare(aa_text, ac_text)
        print('\n')
        for key, start, stop in actions.substrings.common_substrings(collector):
            print(start, stop, key)


if __name__ == '__main__':
    unittest.main(verbosity=2)
