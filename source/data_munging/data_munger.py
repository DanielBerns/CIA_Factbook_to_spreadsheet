from actions.logs import start_logs
from actions.readers import read_root_and_file_with_mimetype
from actions.processors import (FactbookFilesMimetypeProcessor, 
                                iterate_factbooks_files, 
                                create_report)


def main() -> None:
    logger = start_logs('data_munger', 'alpha', 'data_munging/data_munger')
    mimetype_stats = FactbookFilesMimetypeProcessor()
    for factbook, root, filename, mimetype in iterate_factbooks_files():
        mimetype_stats.update(factbook, root, filename, mimetype)
    with create_report('data_munger', 'alpha', 'mimetype_stats.md') as target:
        mimetype_stats.report(target)


if __name__ == '__main__':
    main()
