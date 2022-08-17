from context import actions

from pathlib import Path

import unittest


def print_text(text: str) -> str:
    print('start', text[:80])
    print('end', text[-80:])
    print('length', len(text))

class DataMungingCase(unittest.TestCase):
        
    def test_compare(self):
        a, b = 1, 2
        red = f"testing {a:d} color {b:d}"
        blue = f"testing nada color azul"
        collector = actions.substrings.compare(red, blue)
        print('\n')

    def test_read_html(self):
        print('\n')
        aa_path = Path("~", "Data", "CIA", "factbook", "factbook_html_zip", "factbook-2000", "geos", "aa.html").expanduser()
        aa_text = actions.readers.slurp_text_file(aa_path)
        print_text(aa_text)
        ac_path = Path("~", "Data", "CIA", "factbook", "factbook_html_zip", "factbook-2000", "geos", "aa.html").expanduser()
        ac_text = actions.readers.slurp_text_file(ac_path)
        print_text(ac_text)    
        collector = actions.substrings.compare(aa_text, ac_text)
        print('\n')
        for key, start, stop in actions.substrings.common_substrings(collector):
            print(start, stop, key)

    def test_read_root_and_file(self):
        print('\n')
        directory = Path("~", "Data", "CIA", "factbook", "factbook_html_zip").expanduser()
        for number, (root, a_file) in enumerate(actions.readers.read_root_and_file(directory)):
            print(number, '-', str(root), '-', a_file)
            
    def test_get_root_and_file_with_mimetypes(self):
        print('\n')
        directory = Path("~", "Data", "CIA", "factbook", "factbook_html_zip").expanduser()
        factbook_years = ["factbook-2000", "factbook-2001"]
        for root, a_file, mimetype in actions.readers.read_root_and_file_with_mimetypes(directory):
            print('-', str(root), '-', a_file, ':', mimetype)

    def test_logging(self):
        log_handler = lambda logger: actions.logging.add_stream_handler(logger)
        logger = actions.logging.get_logger('test_logging', log_handler)
        logger.info('We are here at test_logging')


if __name__ == '__main__':
    unittest.main(verbosity=2)
