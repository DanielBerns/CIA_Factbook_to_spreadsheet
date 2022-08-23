from actions.logs import start_logs
from actions.helpers import get_timestamp
from actions.readers import iterate_factbook_files, slurp_text_file
from actions.processors import (FactbookFilesMimetypeProcessor, 
                                FilesPerFactbookProcessor,
                                FactbookFilter,
                                create_report,
                                create_datafile)
from actions.parsers import (Source, Selector, Match, Grab, Repeat, Document, Parser)

from pathlib import Path


def root_fn(root: str) -> bool:
    return root.endswith('fields')


def get_field(field_filepath: Path) -> str:
    p = field_filepath.parts
    field_filename = p[-1]
    q = field_filename.split('.')
    field = q[0]
    return field

   
def main() -> None:
    experiment = 'step_alpha'
    version = get_timestamp()
    Parser.logger = logger = start_logs(experiment, version, 'data_munging/step_alpha.py')
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
    with create_report(experiment, version, 'eda', 'mimetype_stats.md') as target:
        mimetype_stats.report(target)
    with create_report(experiment, version, 'eda', 'field_stats.md') as target:
        files_per_factbook.report(target)        
    for factbook, all_the_field_filepaths in files_per_factbook.store.items():
        with write_datafile(experiment, version, str(Path('fields', factbook)), 'fields.csv') as target:
            for field_filepath in all_the_field_filepaths:
                field = get_field(field_filepath)
                target.write(f'{field:s}\n')
    logger.info('done reports')


if __name__ == '__main__':
    main()
