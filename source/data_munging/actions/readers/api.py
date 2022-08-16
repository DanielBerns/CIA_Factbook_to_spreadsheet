from pathlib import Path 
from typing import Tuple


def slurp_text_file(text_file: Path) -> str:
    text = None
    with open(text_file, 'r') as source:
        text = source.read()
    return text


def readlines_text_file(text_file: Path) -> str:
    with open(text_file, 'r') as source:
        for line in source:
            yield line


def read_filetree(directory: Path) -> Tuple[Path, str]:
    for root, dirs, files in os.walk(directory, topdown=False):
        for a_file in files:
            yield root, a_file

    
def main() -> None:
    print('readers.api.main')
