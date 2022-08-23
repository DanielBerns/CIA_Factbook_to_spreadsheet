from collections import Counter, defaultdict
from typing import (Protocol, Dict, TextIO, List, Optional, Generator, Callable)
from pathlib import Path
from contextlib import contextmanager
from dataclasses import dataclass

from actions.readers import (
    read_factbook_files_event,
    iterate_factbook_files,
    FactbookFilesEvent,
    slurp_text_file,
)
from actions.helpers import get_directory
from actions.config import Config, DATA_DIRECTORY

str_filter_fn = Callable[[str], bool]

def default_str_fn(value: str) -> bool:
    return True

gate_fn = Callable[[List[bool]], bool]

def and_fn(array: List[bool]) -> bool:
    return all(array)

def or_fn(array: List[bool]) -> bool:
    return any(array)

def not_fn(value: bool) -> bool:
    return not value

@dataclass
class FactbookFilter:
    factbook: str_filter_fn = default_str_fn
    root: str_filter_fn = default_str_fn
    filename: str_filter_fn = default_str_fn
    mimetype: str_filter_fn = default_str_fn
    gate: gate_fn = and_fn

    def accepts(self, event: FactbookFilesEvent) -> bool:
        values = []
        values.append(self.factbook(event.factbook))
        values.append(self.root(event.root))
        values.append(self.filename(event.filename))
        values.append(self.mimetype(event.mimetype))
        return self.gate(values)


def filter_factbook_files(
    events_filter: FactbookFilter,
) -> Generator[FactbookFilesEvent, None, None]:
    for event in iterate_factbook_files():
        if events_filter.accepts(event):
            yield event


class FactbookFilesProcessor(Protocol):
    def update(self, event: FactbookFilesEvent) -> None:
        pass

    def report(self, target: TextIO) -> None:
        pass


class FactbookFilesMimetypeProcessor:
    def __init__(self) -> None:
        self._store: Dict = defaultdict(lambda: defaultdict(Counter))

    @property
    def store(self) -> Dict:
        return self._store

    def update(self, event: FactbookFilesEvent) -> None:
        self.store[event.factbook][event.root][event.mimetype] += 1

    def report(self, target: TextIO) -> None:
        for factbook, root_counters in self.store.items():
            target.write(f"{factbook:s}\n")
            for root, mimetype_counters in root_counters.items():
                target.write(f"  {root:s}\n")
                for mimetype, count in mimetype_counters.items():
                    target.write(f"    {str(mimetype):s}: {count:d}\n")


class EventProcessor:
    def __init__(self, store: Dict):
        self._store: Dict = store

    @property
    def store(self) -> Dict:
        return self._store

    def update(self, event: FactbookFilesEvent) -> None:
        raise NotImplementedError()

    def report(self, target: TextIO) -> None:
        raise NotImplementedError()


class FilesPerFactbookProcessor(EventProcessor):
    def __init__(self):
        store = defaultdict(list)
        super().__init__(store)

    def update(self, event: FactbookFilesEvent) -> None:
        file_identifier = Path(event.root, event.filename)
        self.store[event.factbook].append(file_identifier)

    def report(self, target: TextIO) -> None:
        for key, values in self.store.items():
            target.write(f"{str(key):s}\n")
            for v in values:
                target.write(f"  {str(v):s}\n")


class Target(Protocol):
    def report(self, target: TextIO) -> None:
        pass

    
class ContentProcessor:
    def __init__(self, store):
        self._store: Dict = dict()

    @property
    def store(self) -> Dict:
        return self._store

    def update(self, key: str, content: str) -> None:
        self.store[key] = self.transform(content)

    def report(self, target: TextIO) -> None:
        raise NotImplementedError()

    def transform(self, content: str) -> List[Target]:
        raise NotImplementedError()
    


class FactbookFilesContentProcessor:
    def __init__(self, 
                 content_processor: ContentProcessor,
                 event_filter: FactbookFilter) -> None:
        self._content_processor: ContentProcessor = content_processor
        self._event_filter: FactbookFilter = event_filter

    @property
    def content_processor(self) -> ContentProcessor:
        return self._content_processor

    def update(self, event: FactbookFilesEvent) -> None:
        if self.event_filter.accepts(event):
            content = slurp_text_file(Path(event.root, event.filename))
            self.text_processor.update(content)

    def report(self, target: TextIO) -> None:
        self.content_processor.report(target)


@contextmanager
def create_report(experiment: str, version: str, folder: str, filename: str):
    directory = get_directory(Path(Config.REPORTS_DIRECTORY, experiment, version, folder))
    with open(Path(directory, filename), "w") as resource:
        try:
            yield resource
        finally:
            resource.close()

@contextmanager
def create_datafile(experiment: str, version: str, folder: str, filename: str):
    directory = get_directory(Path(Config.REPORTS_DIRECTORY, experiment, version, folder))
    with open(Path(directory, filename), "w") as resource:
        try:
            yield resource
        finally:
            resource.close()
