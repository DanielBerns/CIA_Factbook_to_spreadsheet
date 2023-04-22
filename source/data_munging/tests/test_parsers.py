from context import actions

from pathlib import Path

import unittest

class ParsersTestCase(unittest.TestCase):

    def setUp(self):
        actions.logs.LOGS.info('ParsersTestCase start')
        text_path = Path("~", "Data", "CIA", 
                         "factbook", "factbook_html_zip", "factbook-2000", "fields", 
                         "age_structure.html").expanduser()
        text = actions.readers.slurp_text_file(text_path)
        self.source = actions.parsers.Source(text, end=len(text))
        self.experiment = 'test_parsers'
        self.version = actions.helpers.get_timestamp()

    def tearDown(self):
        actions.logs.LOGS.info('ParsersTestCase stop')
        
    def test_parse_html(self):
        selector = actions.parsers.Selector('<HR SIZE="3" WIDTH="100%" NOSHADE>')
        title_match = actions.parsers.Match('<TITLE>', identifier='title_match')
        title_grab = actions.parsers.Grab('</TITLE>', identifier='title_grab')
        p_skip = actions.parsers.Match('<p>')
        p_grab = actions.parsers.Grab('<p>', identifier='p_grab')
        repeat_p_grab = actions.parsers.Repeat([p_grab])
        document = actions.parsers.Document([title_match, title_grab, p_skip, repeat_p_grab])
        document.process(self.source)
        with actions.processors.create_report(
            self.experiment, self.version, 
            'ParsersTestCase', 'test_parse_html.md') as target:
            target.write('# Age structure\n\n')
            title_grab.report(target)
            target.write('\n\n')
            p_grab.report(target)
            target.write('\n\n')
            document.report(target)
            
    def test_source(self):
        with actions.processors.create_report(
            self.experiment, self.version, 
            'ParsersTestCase', 'test_source.md') as target:
            for character, positions in self.source.table.items():
                target.write(f'{character:s}: ')
                for p in positions:
                    target.write(f'{p:d}, ')
                target.write('\n')


if __name__ == '__main__':
    unittest.main(verbosity=2)
