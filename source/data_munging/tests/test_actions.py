from context import actions as ac

from pathlib import Path

import unittest


def print_text(text: str) -> str:
    print('start', text[:80])
    print('end', text[-80:])
    print('length', len(text))


class DataMungingCase(unittest.TestCase):
        
    def test_main(self):
        print('\n')
        ac.substrings.api.main()
        ac.processors.api.main()
        ac.readers.api.main()

    def test_compare(self):
        a, b = 1, 2
        red = f"testing {a:d} color {b:d}"
        blue = f"testing nada color azul"
        collector = ac.substrings.api.compare(red, blue)
        print('\n')
        # for key, start, stop in ac.substrings.api.show_collector(collector):
        #     print(start, stop, key)

    def test_read_html(self):
        print('\n')
        aa_path = Path("~", "Data", "CIA", "factbook", "factbook_html_zip", "factbook-2000", "geos", "aa.html").expanduser()
        aa_text = ac.readers.api.read_text_file(aa_path)
        print_text(aa_text)
        ac_path = Path("~", "Data", "CIA", "factbook", "factbook_html_zip", "factbook-2000", "geos", "aa.html").expanduser()
        ac_text = ac.readers.api.read_text_file(ac_path)
        print_text(ac_text)    
        collector = ac.substrings.api.compare(aa_text, ac_text)
        print('\n')
        # for key, start, stop in ac.substrings.api.show_collector(collector):
        #     print(start, stop, key)
            
    def test_logging(self):
        log_handler = lambda logger: ac.logging.api.add_stream_handler(logger)
        logger = ac.logging.api.get_logger('test_logging', log_handler)
        logger.info('We are here at test_logging')
    
    def test_eda(self):
        with ac.eda.api.get_target() as target,
             ac.eda.api.get_source() as source,
             for event in source.read():
                 target.update(event)


if __name__ == '__main__':
    unittest.main(verbosity=2)
