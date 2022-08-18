from collections import Counter, defaultdict
from typing import Protocol, Dict, Tuple, TextIO
from pathlib import Path
from contextlib import contextmanager

from actions.readers import read_root_and_file_with_mimetype
from actions.helpers import get_directory
from actions.config import Config, DATA_DIRECTORY

FIRST_YEAR = 2000
LAST_YEAR = 2020

def iterate_factbooks_files() -> Tuple[str, Path, str, str]:
    factbooks = [f'factbook-{year:d}' for year in range(FIRST_YEAR, LAST_YEAR + 1)]
    for a_factbook in factbooks:
        a_factbook_base = Path(DATA_DIRECTORY, a_factbook)
        for root, filename, mimetype in read_root_and_file_with_mimetype(a_factbook_base):
            yield a_factbook, root, filename, mimetype


class FactbookFilter:
    def accepts(factbook: str, root: Path, filename: str, mimetype: str) -> bool:
        pass


def filter_factbooks_files(events_filter: FactbookFilter) -> Tuple[str, Path, str, str]:
    for factbook, root, filename, mimetype in iterate_factbooks_files():
        if events_filter.accepts(factbook, root, filename, mimetype):
            yield factbook, root, filename, mimetype


class FactbookFilesProcessor(Protocol):
    def update(self, factbook: str, root: Path, filename: str, mimetype: str) -> None:
        pass
    
    def report(self, target: TextIO) -> None:
        pass


class TextProcessor(Protocol):
    def mimetype(self) -> str:
        pass

    def update(self, text: str) -> None:
        pass
    
    def report(self, target: TextIO) -> None:
        pass
    
    
class FactbookFilesMimetypeProcessor:
    def __init__(self):
        self._mimetypes_per_factbook = defaultdict(Counter)
        
    @property
    def mimetypes_per_factbook(self):
        return self._mimetypes_per_factbook
        
    def update(self, factbook: str, root: Path, filename: str, mimetype: str) -> None:
        self.mimetypes_per_factbook[factbook][mimetype] += 1
    
    def report(self, target: TextIO) -> None:
        for factbook, mimetype_counters in self.mimetypes_per_factbook.items():
            target.write(f'{factbook:s}\n')
            for mimetype, count in mimetype_counters.items():
                target.write(f'  {str(mimetype):s}: {count:d}\n')        


class FactbookFilesPatternsProcessor:
    def __init__(self, patterns: TextProcessor):
        self._patterns = patterns
        
    @property
    def patterns(self):
        return self._patterns
    
    def update(self, factbook: str, root: Path, filename: str, mimetype: str) -> None:
        if mimetype != self.patterns.mimetype():
            return
        text = actions.readers.slurp_text_file(Path(root, filename))
        self.patterns.extract(text)
    
    def report(self, target: TextIO) -> None:
        self.patterns.report(target)

@contextmanager
def create_report(experiment: str, version: str, filename: str):
    directory = get_directory(Path(Config.REPORTS_DIRECTORY, experiment, version))
    with open(Path(directory, filename), 'w') as resource:
        try:
            yield resource
        finally:
            resource.close()


if __name__ == '__main__':
    main()
