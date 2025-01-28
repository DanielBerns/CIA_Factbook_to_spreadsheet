from context import components

from pathlib import Path

import unittest

def print_text(text: str) -> None:
    print('start', text[:80])
    print('end', text[-80:])
    print('length', len(text))


class ComponentsTestCase(unittest.TestCase):

    def setUp(self):
        print('setup')
        
    def tearDown(self):
        print('tearDown')
        
    def test_storage(self):
        storage = components.core.Storage('cia_factbook', 'datamunging', 'bravo')
        print(storage.dotenv)
        print(storage.base)
        print(storage.inputs)
        print(storage.outputs)
        print(storage.reports)
        print(storage.logs)
        print(storage.commands)
        
    def test_helpers_json(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
