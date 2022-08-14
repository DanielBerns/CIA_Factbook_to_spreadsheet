import logging
from pathlib import Path

from typing import Callable

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
    logs_base: Path,
    logging_name,
    logging_level: int = logging.DEBUG
    ) -> None:
    file_handler = RotatingFileHandler(
        Path(logs_base, logging_name),
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
