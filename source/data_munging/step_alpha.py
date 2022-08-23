from actions.logs import start_logs
from actions.helpers import get_timestamp
from actions.readers import iterate_factbook_files, slurp_text_file
from actions.processors import (FactbookFilesMimetypeProcessor, 
                                FilesPerFactbookProcessor,
                                FactbookFilter,
                                create_report)
from actions.parsers import (Source, Selector, Match, Grab, Repeat, Document, Parser)

from pathlib import Path

experiment = 'data_munger'
version = get_timestamp()

def root_fn(root: str) -> bool:
    return root.endswith('fields')

def get_fb_2000_fields_age_structure() -> None:
    text_path = Path("~", "Data", "CIA", 
                     "factbook", "factbook_html_zip", "factbook-2000", "fields", 
                     "age_structure.html").expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('<HR SIZE="3" WIDTH="100%" NOSHADE>')
    title_match = Match('<TITLE>', identifier='title_match')
    title_grab = Grab('</TITLE>', identifier='title_grab')
    p_skip = Match('<p>')
    p_grab = Grab('<p>', identifier='p_grab')
    repeat_p_grab = Repeat([p_grab])
    document = Document([title_match, title_grab, p_skip, repeat_p_grab])
    document.process(source)
    with create_report(experiment, version, 'eda', 'fb_2000-fields-age_structure_html.md') as target:
        target.write('# Age structure\n\n')
        title_grab.report(target)
        target.write('\n\n')
        p_grab.report(target)
        target.write('\n\n')
        document.report(target)


def get_fb_2000_fields_administrative_divisions() -> None:
    text_path = Path("~", "Data", "CIA", 
                     "factbook", "factbook_html_zip", "factbook-2000", "fields", 
                     "administrative_divisions.html").expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('<HR SIZE="3" WIDTH="100%" NOSHADE>')
    title_match = Match('<TITLE>', identifier='title_match')
    title_grab = Grab('</TITLE>', identifier='title_grab')
    p_skip = Match('<p>')
    p_grab = Grab('<p>', identifier='p_grab')
    repeat_p_grab = Repeat([p_grab])
    document = Document([title_match, title_grab, p_skip, repeat_p_grab])
    document.process(source)
    with create_report(experiment, version, 'eda', 'fb_2000-fields-administrative_divisions_html.md') as target:
        target.write('# administrative divisions\n\n')
        title_grab.report(target)
        target.write('\n\n')
        p_grab.report(target)
        target.write('\n\n')
        document.report(target)


def get_fb_2000_fields(field: str) -> None:
    text_path = Path("~", "Data", "CIA", 
                     "factbook", "factbook_html_zip", "factbook-2000", "fields", 
                     field + '.html').expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('<HR SIZE="3" WIDTH="100%" NOSHADE>')
    title_match = Match('<TITLE>', identifier='title_match')
    title_grab = Grab('</TITLE>', identifier='title_grab')
    p_skip = Match('<p>')
    p_grab = Grab('<p>', identifier='p_grab')
    repeat_p_grab = Repeat([p_grab])
    document = Document([title_match, title_grab, p_skip, repeat_p_grab])
    document.process(source)
    with create_report(experiment, version, 'eda', f'fb_2000-fields-{field:s}_html.md') as target:
        target.write(f'# {field:s}\n\n')
        title_grab.report(target)
        target.write('\n\n')
        p_grab.report(target)
        target.write('\n\n')
        document.report(target)

def get_field(path: Path) -> str:
    p = field_file_path.parts
    field_filename = p[-1]
    q = field_filename.split('.')
    field = q[0]
    return field
   
def main() -> None:
    Parser.logger = logger = start_logs(experiment, version, 'data_munging/data_munger.py')
    mimetype_stats = FactbookFilesMimetypeProcessor()
    root_filter = FactbookFilter(root=root_fn)
    files_per_factbook = FilesPerFactbookProcessor()
    logger.info('before iterate_factbook_files')
    for number, event in enumerate(iterate_factbook_files()):
        mimetype_stats.update(event)
        if root_filter.accepts(event):
            files_per_factbook.update(event)
    logger.info('after iterate_factbook_files')

    logger.info('starting reports')
    with create_report(experiment, version, [], 'mimetype_stats.md') as target:
        mimetype_stats.report(target)
    with create_report(experiment, version, 'field_stats.md') as target:
        files_per_factbook.report(target)        
    for factbook, all_the_field_filepaths in files_per_factbook.store.items():
        with create_datafile(experiment, version, ['fields', factbook], 'fields.csv') as target:
            for field_file_path in all_the_field_filepaths:
                field = get_field(field_filepath)
                target.write(f'{field:s}\n')
    logger.info('done reports')


if __name__ == '__main__':
    main()
