from context import actions

from collections import Counter, defaultdict

import unittest


class ScrapCase(unittest.TestCase):
        
    def test_mimetype_with_counters_standardlib(self):
        mimetypes_per_factbook = defaultdict(Counter)
        for factbook, root, filename, mimetype in actions.processors.iterate_factbooks_files():
            mimetypes_per_factbook[factbook][mimetype] += 1
            
        for factbook, mimetype_counters in mimetypes_per_factbook.items():
            print(factbook)
            for mimetype, count in mimetype_counters.items():
                print('  ', mimetype, count)


if __name__ == '__main__':
    unittest.main(verbosity=2)
