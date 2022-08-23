from actions.logs import start_logs
from actions.helpers import get_timestamp
from actions.readers import iterate_factbook_files, slurp_text_file
from actions.processors import (FactbookFilesMimetypeProcessor, 
                                FilesPerFactbookProcessor,
                                FactbookFilter,
                                create_report,
                                read_datafile,
                                write_datafile)
from actions.parsers import (Source, Selector, Match, Grab, Repeat, Document, Parser)
from actions.config import WORLD_FACTBOOK_RAW_DATA

from pathlib import Path

experiment = 'step_bravo'
version = get_timestamp()

def root_fn(root: str) -> bool:
    return root.endswith('fields')


def get_factbook_fields(factbook: str, field: str) -> None:
    # factbook = "factbook-2000"
    text_path = Path(WORLD_FACTBOOK_RAW_DATA, 
                     factbook, "fields", 
                     field + '.html').expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('<HR SIZE="3" WIDTH="100%" NOSHADE>')
    title_match = Match('<TITLE>', identifier='title_match')
    title_grab = Grab('</TITLE>', identifier='title_grab')
    p_skip = Match('<p>')
    p_grab = Grab('<p>', identifier='p_grab')
    repeat_p_grab = Repeat([p_grab])
    document = Document([title_match, title_grab, p_skip, selector, repeat_p_grab])
    document.process(source)
    
    with write_datafile(experiment, version, factbook, f'{field:s}_html.md') as target:
        target.write(f'# {field:s}\n\n')
        title_grab.report(target)
        target.write('\n\n')
        p_grab.report(target)
        target.write('\n\n')
        document.report(target)

   
def main() -> None:
    experiment = 'step_bravo'
    version = get_timestamp()
    Parser.logger = logger = start_logs(experiment, version, 'data_munging/step_bravo.py')

    factbook = "factbook-2000"
    timestamp = "202208231713"
    
    logger.info(f'{experiment:s} - {version:s} start')
    logger.info(f'get_factbook_fields start: {factbook:s} - {timestamp:s}')
    
    with read_datafile('step_alpha', timestamp, str(Path('fields', factbook)), 'fields.csv') as source:
        for line in source:
            field = line[:-1]
            logger.info(f'{factbook:s}: {field:s}')
            get_factbook_fields(factbook, field)
    logger.info(f'get_factbook_fields done: {factbook:s} - {timestamp:s}')
    logger.info(f'{experiment:s} - {version:s} done')

if __name__ == '__main__':
    main()
