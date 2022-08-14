import logging

from actions.core.api import get_logger, add_stream_handler

def main() -> None:
    logger = get_logger(__file__)
    add_stream_handler(logger, logging.DEBUG)
    logger.info('this is a test')
    
if __name__ == '__main__':
    main()
