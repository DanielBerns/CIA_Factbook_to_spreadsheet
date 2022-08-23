from typing import List, TextIO, Optional, Protocol, Dict, DefaultDict, Tuple
from collections import defaultdict
import logging

Table = DefaultDict[str, List[int]]

def get_table(content: str) -> Table:
    table = defaultdict(list)
    for p, c in enumerate(content):
        table[c].append(p)
    return table


class Source:
    def __init__(self, content: str, begin: int = 0, end: int = -1) -> None:
        assert 0 <= begin < len(content)
        assert 0 < end <= len(content)
        assert begin < end
        self._content: str = content
        self._begin: int = begin
        self._end: int = end
        self._cursor: int = begin
        self._table: Table = get_table(content)

    @property
    def content(self) -> str:
        return self._content[self.begin: self.end]

    @property
    def begin(self):
        return self._begin
    
    @property
    def end(self):
        return self._end
    
    @end.setter
    def end(self, value):
        if self.begin <= value < self.end:
            self._end = value

    @property
    def cursor(self):
        return self._cursor
    
    @cursor.setter
    def cursor(self, value):
        self._cursor = value if self.begin <= value <= self.end else self.end

    @property
    def table(self) -> Table:
        return self._table

    def match(self, prefix: str) -> bool:
        if self.cursor >= self.end:
            return False
        p = self.content.find(prefix, self.cursor, self.end)
        if p < 0:
            return False
        else:
            self.cursor = p + len(prefix)
            return True
        
    def grab(self, suffix: str) -> Tuple[bool, Optional[str]]:
        if self.cursor >= self.end:
            return False, None
        p = self.content.find(suffix, self.cursor, self.end)
        if p < 0:
            return False, self.content[self.cursor: self.end]
        else:
            info = self.content[self.cursor: p]
            self.cursor = p + len(suffix)
            return True, info

    def discard_suffix(self, suffix: str) -> bool:
        if self.cursor >= self.end:
            return False
        p = self.content.find(suffix, self.cursor, self.end)
        self.end = p
        return p > 0

       
class Parser:
    logger: Optional[logging.Logger] = None

    def __init__(self, identifier: str = 'Parser') -> None:
        assert Parser.logger is not None
        self._identifier: str = identifier

    @property
    def identifier(self) -> str:
        return self._identifier

    def process(self, source: Source) -> bool:
        return False


class Selector(Parser):
    def __init__(self, suffix: str, identifier: str = 'Selector') -> None:
        super().__init__(identifier)
        self._suffix: str = suffix

    @property
    def suffix(self) -> str:
        return self._suffix

    def process(self, source: Source) -> bool:
        matched = True
        matched = source.discard_suffix(self.suffix)
        Parser.logger.info(f'{self.identifier:s}.process: discard_suffix({self.suffix:s}) == {str(matched):s}')
        return matched


class Match(Parser):
    def __init__(self, prefix: str, identifier: str = 'Match') -> None:
        super().__init__(identifier)
        self._prefix: str = prefix

    @property
    def prefix(self) -> str:
        return self._prefix
    
    def process(self, source: Source) -> bool:
        matched = source.match(self.prefix)
        Parser.logger.info(f'{self.identifier:s}.process: match({self.prefix:s}) == {str(matched):s}')            
        return matched


def simplify(string: str):
    a = string.replace('\n', ' ')
    b = ' '.join(a.split())
    return b


class Grab(Parser):
    def __init__(self, suffix: str, identifier: str = 'Grab') -> None:
        super().__init__(identifier)
        self._suffix: str = suffix
        self._store: List[str] = list()
            
    @property
    def suffix(self) -> str:
        return self._suffix
    
    @property
    def identifier(self) -> str:
        return self._identifier
    
    @property
    def store(self) -> List[str]:
        return self._store

    def process(self, source: Source) -> bool:
        grabbed, value = source.grab(self.suffix)
        # Parser.logger.info(f'{self.identifier:s}.process: grab({self.suffix:s}) == {grabbed}')            
        # Parser.logger.info(f'  {value:s}')
        self.store.append(simplify(value))
        return grabbed

    def report(self, target: TextIO) -> None:
        target.write(f'## {self.identifier:s}\n')
        for value in self.store:
            target.write(f'  {value:s}\n')
        target.write('\n')

class Sequence(Parser):
    
    def __init__(self, fragments: List[Parser], identifier: str = 'Sequence') -> None:
        super().__init__(identifier)
        self._fragments: List[Parser] = fragments
        
    @property
    def fragments(self) -> List[Parser]:
        return self._fragments
    
    def process(self, source: Source) -> bool:
        matched = True
        for parser in self.fragments:
            matched = parser.process(source)
            if not matched:
                break
        return matched


class Repeat(Sequence):

    def __init__(self, fragments: List[Parser], identifier: str = 'Repeat') -> None:
        super().__init__(fragments, identifier=identifier)

    def process(self, source: Source) -> bool:
        Parser.logger.info(f'Repeat.process start')        
        pass_counter = 0
        matched = super().process(source) 
        Parser.logger.info(f'Repeat.process: {self.identifier:s} pass #{pass_counter:d} == {str(matched):s}')
        while matched:
            pass_counter += 1
            matched = super().process(source)
            Parser.logger.info(f'Repeat.process: {self.identifier:s} pass #{pass_counter:d} == {str(matched):s}')
        Parser.logger.info(f'Repeat.process done')        


class Document(Sequence):
    def __init__(self, fragments: List[Parser], identifier: str = 'Document') -> None:
        super().__init__(fragments, identifier=identifier)

    def process(self, source: Source) -> bool:
        matched = super().process(source)
        Parser.logger.info(f'Document.process: {self.identifier:s} == {str(matched):s}')
    
    def report(self, target: TextIO) -> None:
        target.write(f'## {self.identifier:s}\n')
        target.write('\n')

