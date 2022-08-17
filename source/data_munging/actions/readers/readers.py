import os
from pathlib import Path 
from typing import Tuple
import mimetypes

def slurp_text_file(text_file: Path) -> str:
    text = None
    with open(text_file, 'r') as source:
        text = source.read()
    return text


def readlines_text_file(text_file: Path) -> str:
    with open(text_file, 'r') as source:
        for line in source:
            yield line


def read_root_and_file(directory: Path) -> Tuple[Path, str]:
    for root, dirs, files in os.walk(directory, topdown=False):
        for a_file in files:
            yield root, a_file


def read_root_and_file_with_mimetype(directory: Path) -> Tuple[Path, str, str]:
    for root, a_file in read_root_and_file(directory):
        a_file_mimetype = mimetypes.guess_type(Path(root, a_file))
        yield root, a_file, a_file_mimetype[0]


def main() -> None:
    print('readers.api.main')
