from actions.logs import start_logs
from actions.readers import read_root_and_file_with_mimetype
from actions.processors import (FactbookFilesMimetypeProcessor, 
                                iterate_factbooks_files, 
                                create_report)


def main() -> None:
    logger = start_logs('data_munger', 'alpha', 'data_munging/data_munger')
    mimetype_stats = FactbookFilesMimetypeProcessor()
    logger.info('before iterate_factbooks_files')
    for number, (factbook, root, filename, mimetype) in enumerate(iterate_factbooks_files()):
        mimetype_stats.update(factbook, root, filename, mimetype)
    logger.info('after iterate_factbooks_files')
    logger.info('starting reports')
    with create_report('data_munger', 'alpha', 'mimetype_stats.md') as target:
        mimetype_stats.report(target)
    logger.info('done reports')


if __name__ == '__main__':
    main()
