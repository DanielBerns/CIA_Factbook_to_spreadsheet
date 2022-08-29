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
import logging

experiment = 'step_bravo'
version = get_timestamp()

def root_fn(root: str) -> bool:
    return root.endswith('fields')


def get_fields_factbook_2000(factbook: str, field: str) -> None:
    assert factbook == "factbook-2000"
    text_path = Path(WORLD_FACTBOOK_RAW_DATA, 
                     factbook, "fields", 
                     field + '.html').expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('<HR SIZE="3" WIDTH="100%" NOSHADE>')
    title_match = Match('<TITLE>', identifier='title_match')
    title_grab = Grab('</TITLE>', identifier='title_grab')
    data_start = Match('<p>')
    data_grab = Grab('<p>', identifier='p_grab')
    repeat_data_grab = Repeat([data_grab])
    document = Document([title_match, title_grab, data_start, selector, repeat_data_grab])
    document.process(source)
    with write_datafile(experiment, version, factbook, f'{field:s}_html.md') as target:
        target.write(f'# {field:s}\n\n')
        title_grab.report(target)
        target.write('\n\n')
        data_grab.report(target)
        target.write('\n\n')
        document.report(target)



def get_fields_factbook_2001(factbook: str, field: str) -> None:
    assert factbook == "factbook-2001"
    text_path = Path(WORLD_FACTBOOK_RAW_DATA, 
                     factbook, "fields", 
                     field + '.html').expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('</body>')
    title_match = Match('<title>', identifier='title_match')
    title_grab = Grab('</title>', identifier='title_grab')
    table_end = Match('</table>')
    data_start = Match('<font face="arial" size="2">')
    data_grab = Grab('<font face="arial" size="2">', identifier='data_grab')
    repeat_data_grab = Repeat([data_grab])
    document = Document([title_match, title_grab, table_end, data_start, selector, repeat_data_grab])
    document.process(source)
    with write_datafile(experiment, version, factbook, f'{field:s}_html.md') as target:
        target.write(f'# {field:s}\n\n')
        title_grab.report(target)
        target.write('\n\n')
        data_grab.report(target)
        target.write('\n\n')
        document.report(target)

# <table width="90%" cellspacing="0" cellpadding="4" border="1" bgcolor="#FFFFFF" align="center">
def get_fields_factbook_2002(factbook: str, field: str) -> None:
    assert factbook == "factbook-2002"
    text_path = Path(WORLD_FACTBOOK_RAW_DATA, 
                     factbook, "fields", 
                     field + '.html').expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('</body>')
    title_match = Match('<title>', identifier='title_match')
    title_grab = Grab('</title>', identifier='title_grab')

    data_start = Match('<table width="90%" cellspacing="0" cellpadding="4" border="1" bgcolor="#FFFFFF" align="center">')
    data_grab = Grab('</table>', identifier='data_grab')
    repeat_data_grab = Repeat([data_grab])
    document = Document([title_match, title_grab, data_start, selector, repeat_data_grab])
    document.process(source)
    with write_datafile(experiment, version, factbook, f'{field:s}_html.md') as target:
        target.write(f'# {field:s}\n\n')
        title_grab.report(target)
        target.write('\n\n')
        data_grab.report(target)
        target.write('\n\n')
        document.report(target)


def get_fields(experiment: str, version: str, factbook: str, timestamp: str):    
    with read_datafile('step_alpha', timestamp, str(Path('fields', factbook)), 'fields.csv') as source:
        for line in source:
            field = line[:-1]
            yield field


def main() -> None:

    Parser.logger = logger = start_logs(experiment, version, 'data_munging/step_bravo.py')

    step_alpha_timestamp = "202208231713"

    factbook = "factbook-2000"
    logger.info(f'{experiment:s} - {version:s} start')
    logger.info(f'get_fields start: {factbook:s} - {step_alpha_timestamp:s}')
    for field in get_fields(experiment, version, factbook, step_alpha_timestamp):
        get_fields_factbook_2000(factbook, field)
    logger.info(f'get_fields done: {factbook:s} - {step_alpha_timestamp:s}')
    logger.info(f'{experiment:s} - {version:s} done')

    factbook = "factbook-2001"
    logger.info(f'{experiment:s} - {version:s} start')
    logger.info(f'get_fields start: {factbook:s} - {step_alpha_timestamp:s}')
    for field in get_fields(experiment, version, factbook, step_alpha_timestamp):
        get_fields_factbook_2001(factbook, field)
    logger.info(f'get_fields done: {factbook:s} - {step_alpha_timestamp:s}')
    logger.info(f'{experiment:s} - {version:s} done')

    factbook = "factbook-2002"
    logger.info(f'{experiment:s} - {version:s} start')
    logger.info(f'get_fields start: {factbook:s} - {step_alpha_timestamp:s}')
    for field in get_fields(experiment, version, factbook, step_alpha_timestamp):
        get_fields_factbook_2002(factbook, field)
    logger.info(f'get_fields done: {factbook:s} - {step_alpha_timestamp:s}')
    logger.info(f'{experiment:s} - {version:s} done')

if __name__ == '__main__':
    main()
