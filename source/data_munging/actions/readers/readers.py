import os
from pathlib import Path
from typing import Tuple, Generator
import mimetypes
from dataclasses import dataclass

from actions.config import WORLD_FACTBOOK_RAW_DATA


def slurp_text_file(text_file: Path) -> str:
    text = None
    with open(text_file, "r") as source:
        text = source.read()
    return text


def readlines_text_file(text_file: Path) -> Generator[str, None, None]:
    with open(text_file, "r") as source:
        for line in source:
            yield line


@dataclass
class FactbookFilesEvent:
    factbook: str
    label: str
    filename: str
    mimetype: str


def read_factbook_files_event(
    factbook: str, directory: Path = WORLD_FACTBOOK_RAW_DATA
) -> Generator[FactbookFilesEvent, None, None]:
    base = Path(directory, factbook)
    for root, dirs, files in os.walk(base, topdown=False):
        for filename in files:
            file_mimetype = mimetypes.guess_type(Path(root, filename))
            yield FactbookFilesEvent(factbook, root, filename, str(file_mimetype))


FIRST_YEAR: int = 2000
LAST_YEAR: int = 2020


def iterate_factbook_events(
    first_year: int = FIRST_YEAR, last_year: int = LAST_YEAR
) -> Generator[FactbookFilesEvent, None, None]:
    assert FIRST_YEAR <= first_year <= LAST_YEAR
    assert FIRST_YEAR <= last_year <= LAST_YEAR
    assert first_year <= last_year
    factbooks = [f"factbook-{year:d}" for year in range(first_year, last_year + 1)]
    for a_factbook in factbooks:
        for event in read_factbook_files_event(a_factbook):
            yield event
