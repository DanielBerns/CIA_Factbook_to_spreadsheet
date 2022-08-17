from collections import Counter, defaultdict
from config import Config, DATA_DIRECTORY


from actions.logs import get_logger, add_stream_handler, add_rotating_file_handler
from actions.readers import read_root_and_file_with_mimetype
from typing import Tuple
from pathlib import Path

FIRST_YEAR = 2000
LAST_YEAR = 2020

def start_logs() -> None:
    log_handler = None
    if Config.LOG_TO_STDOUT == "YES":
        log_handler = lambda logger: add_stream_handler(logger)
    else:
        log_handler = lambda logger: add_rotating_file_handler(
            logger, 
            reports_directory=Config.REPORTS_DIRECTORY)        
    logger = get_logger('data_munger', log_handler)
    logger.info(f'We are here at data_munging/data_munger.py')
    return logger


def iterate_factbooks_files() -> Tuple[str, Path, str, str]:
    factbooks = [f'factbook-{year:d}' for year in range(FIRST_YEAR, LAST_YEAR + 1)]
    for a_factbook in factbooks:
        a_factbook_base = Path(DATA_DIRECTORY, a_factbook)
        for root, filename, mimetype in read_root_and_file_with_mimetype(a_factbook_base):
            # print('-', str(root), '-', filename, ':', mimetype)
            yield a_factbook, root, filename, mimetype


def main() -> None:
    logger = start_logs()
    mimetypes_per_factbook = defaultdict(Counter)
    for factbook, root, filename, mimetype in iterate_factbooks_files():
        mimetypes_per_factbook[factbook][mimetype] += 1
        
    for factbook, mimetype_counters in mimetypes_per_factbook.items():
        print(factbook)
        logger.info(factbook)
        for mimetype, count in mimetype_counters.items():
            print('  ', mimetype, count)

    
if __name__ == '__main__':
    main()
