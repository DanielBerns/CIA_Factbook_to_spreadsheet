from collections import Counter, defaultdict
from typing import (Protocol, Dict, TextIO, List, Optional, Generator, Callable)
from pathlib import Path
from contextlib import contextmanager
from dataclasses import dataclass

from actions.readers import (
    read_factbook_files_event,
    iterate_factbook_events,
    FactbookFilesEvent,
    slurp_text_file,
)
from actions.helpers import get_directory
from actions.config import Config

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
    label: str_filter_fn = default_str_fn
    filename: str_filter_fn = default_str_fn
    mimetype: str_filter_fn = default_str_fn
    gate: gate_fn = and_fn

    def accepts(self, event: FactbookFilesEvent) -> bool:
        values = []
        values.append(self.factbook(event.factbook))
        values.append(self.label(event.label))
        values.append(self.filename(event.filename))
        values.append(self.mimetype(event.mimetype))
        return self.gate(values)


def filter_factbook_events(
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


class EventCounterProcessor(EventProcessor):
    def __init__(self) -> None:
        store = Counter()
        super().__init__(store)

    def update(self, event: FactbookFilesEvent) -> None:
        self.store[event.factbook] += 1
        self.store[event.label] += 1        
        self.store[event.mimetype] += 1

    def report(self, target: TextIO) -> None:
        for key, value in self.store.items():
            target.write(f'{key:s}: {value:d}\n')


class FactbookFilesMimetypeProcessor(EventProcessor):
    def __init__(self) -> None:
        store: Dict = defaultdict(
            lambda: defaultdict(
                Counter))
        super().__init(store)

    def update(self, event: FactbookFilesEvent) -> None:
        self.store[event.factbook][event.label][event.mimetype] += 1

    def report(self, target: TextIO) -> None:
        for factbook, label_counters in self.store.items():
            target.write(f"{factbook:s}\n")
            for label, mimetype_counters in label_counters.items():
                target.write(f"  {root:s}\n")
                for mimetype, count in mimetype_counters.items():
                    target.write(f"    {str(mimetype):s}: {count:d}\n")


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
def create_report(
    experiment: str, 
    version: str, 
    label: str, 
    filename: str,
    directory: Path = Config.APPLICATION_REPORTS
    ):
    base = get_directory(Path(directory, experiment, version, label))
    with open(Path(directory, filename), "w") as resource:
        try:
            yield resource
        finally:
            resource.close()


@contextmanager
def write_file(
    experiment: str, 
    version: str, 
    label: str, 
    filename: str,
    directory: Path = Config.APPLICATION_DATA):
    base = get_directory(Path(directory, experiment, version, label))
    with open(Path(base, filename), "w") as resource:
        try:
            yield resource
        finally:
            resource.close()

@contextmanager
def read_file(
    experiment: str, 
    version: str, 
    label: str, 
    filename: str,
    directory: Path = Config.APPLICATION_DATA):
    base = get_directory(Path(directory, experiment, version, label))
    with open(Path(base, filename), "r") as resource:
        try:
            yield resource
        finally:
            resource.close()
