import logging.handlers
from pathlib import Path

from typing import Callable

from actions.config import Config
from actions.helpers import get_directory


def logs_path(
    reports_directory: Path
    ) -> Path:
    return get_directory(Path(reports_directory, 'logs'))

def add_stream_handler(
    logger: logging.Logger,
    logging_level: int = logging.INFO
    ) -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging_level)
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def add_rotating_file_handler(
    logger: logging.Logger,
    reports_directory: Path,
    logging_level: int = logging.DEBUG
    ) -> None:
    file_handler = logging.handlers.RotatingFileHandler(
        Path(logs_path(reports_directory), 'logs.txt'),
        maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging_level)
    logger.addHandler(file_handler)


def get_logger(
    name: str, 
    add_handler: Callable[[logging.Logger], None],
    logging_level: int = logging.INFO
    ):
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)
    add_handler(logger)
    return logger


def start_logs(experiment: str, version: str, codepoint: str) -> None:
    log_handler = None
    if Config.LOG_TO_STDOUT == "YES":
        log_handler = lambda logger: add_stream_handler(logger)
    else:
        log_handler = lambda logger: add_rotating_file_handler(
            logger, 
            reports_directory=Config.REPORTS_DIRECTORY)        
    logger = get_logger(f'{experiment:s}-{version:s}', log_handler)
    logger.info(f'We are here at {experiment:s}:{version:s} - {codepoint:s}')
    return logger
