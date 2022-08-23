from actions.logs import start_logs
from actions.helpers import get_timestamp
from actions.readers import iterate_factbook_files, slurp_text_file
from actions.processors import (FactbookFilesMimetypeProcessor, 
                                FilesPerFactbookProcessor,
                                FactbookFilter,
                                create_report)
from actions.parsers import (Source, Selector, Match, Grab, Repeat, Document, Parser)

from pathlib import Path

experiment = 'extract_factbook_fields'
version = get_timestamp()

def root_fn(root: str) -> bool:
    return root.endswith('fields')



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
    with create_report(experiment, version, f'fb_2000-fields-{field:s}_html.md') as target:
        target.write(f'# {field:s}\n\n')
        title_grab.report(target)
        target.write('\n\n')
        p_grab.report(target)
        target.write('\n\n')
        document.report(target)

   
def main() -> None:
    logger = start_logs(experiment, version, 'data_munging/extract_factbook_fields.py')

    # ~/Reports/data_munging/CIA_World_Factbook_Albatros/data_munger/202208221753/field_stats.md
    logger.info('get_factbook_fields')
    report_fields_stats = Path(
    with open(report_fields_stats) as source:
        for line in source:
            if line[0] == ' ':
                pass
            else:

    # logger.info('get_fb_2000_fields start')
    # with open('./data/2000_fields.csv') as source:
    #     for line in source:
    #         field = line[:-1]
    #         logger.info(f'get_2000_fields: {field:s}')
    #         get_fb_2000_fields(field)
    # logger.info('get_fb_2000_fields done')


    
    logger.info('starting reports')
    with create_report(experiment, version, 'mimetype_stats.md') as target:
        mimetype_stats.report(target)
    with create_report(experiment, version, 'field_stats.md') as target:
        files_per_factbook.report(target)        
    logger.info('done reports')


if __name__ == '__main__':
    main()
