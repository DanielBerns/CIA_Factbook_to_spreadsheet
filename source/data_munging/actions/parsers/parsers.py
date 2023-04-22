from typing import List, TextIO, Optional, Protocol, Dict, DefaultDict, Tuple
from collections import defaultdict


Table = DefaultDict[str, List[int]]

def get_table(content: str) -> Table:
    table = defaultdict(list)
    for position, c in enumerate(content):
        table[c].append(position)
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
        position = self.content.find(prefix, self.cursor, self.end)
        if position < 0:
            return False
        else:
            self.cursor = position + len(prefix)
            return True
        
    def grab(self, suffix: str) -> Tuple[bool, Optional[str]]:
        if self.cursor >= self.end:
            return False, None
        position = self.content.find(suffix, self.cursor, self.end)
        if position < 0:
            return False, self.content[self.cursor: self.end]
        else:
            info = self.content[self.cursor: position]
            self.cursor = position + len(suffix)
            return True, info

    def discard_suffix(self, suffix: str) -> bool:
        if self.cursor >= self.end:
            return False
        position = self.content.find(suffix, self.cursor, self.end)
        self.end = position
        return position > 0

    def extract_tag(self, tagname: str) -> Tuple[bool, str]:
        if self.cursor >= self.end:
            return False
        prefix = f'<{tagname:s} '
        suffix = '>'
        left = self.content.find(prefix, self.cursor, self.end)
        if left < 0:
            return False, self.content[self.cursor: self.end]
        else:
            left += len(prefix)
            right = self.content.find(suffix, left)
            if right < 0:
                return False, self.content[left: self.end]
            else:
                self.cursor = right
                return True, self.content[left: right]


class Parser:
    def __init__(self, identifier: str = 'Parser') -> None:
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
        return matched

    
class SearchTag(Parser):
    def __init__(self, 
                 tagname: str, 
                 expected_attributes: Dict[str, str],
                 identifier: str = 'SearchTag') -> None:
        super().__init__(identifier)
        self._tagname: str = tagname
        self._expected_attributes: Dict[str, str] = expected_attributes
        
    @property
    def tagname(self) -> str:
        return self._tagname

    @property
    def expected_attributes(self) -> Dict[str, str]:
        return self._expected_attributes

    def verify_attributes(self, extracted_attributes: Dict[str, str]) -> bool:
        tests = [self.expected_attributes.get(key, None) == value for key, value in extracted_attributes.items()]
        return all(tests)                
        
    def get_tag_and_attributes(self, source: Source) -> bool:
        extracted, content = source.extract_tag(self.tagname)
        if extracted:
            if content:
                extracted_attributes = dict()
                simple_content = simplify(content)
                parts = simple_content.split(' ')
                for a_part in parts:
                    try:
                        (key, value) = a_part.split('=')
                        extracted_attributes[key] = value
                    except ValueError:
                        break
                return self.verify_attributes(extracted_attributes)
            else:
                return False
        else:
            return False

    def process(self, source: Source) -> bool:
        go_on = source.cursor < source.end and not self.get_tag_and_attributes(source)
        while go_on:
            go_on = source.cursor < source.end and not self.get_tag_and_attributes(source)
        return source.cursor < source._end
    

class Match(Parser):
    def __init__(self, prefix: str, identifier: str = 'Match') -> None:
        super().__init__(identifier)
        self._prefix: str = prefix

    @property
    def prefix(self) -> str:
        return self._prefix
    
    def process(self, source: Source) -> bool:
        return source.match(self.prefix)


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
        pass_counter = 0
        matched = super().process(source) 
        while matched:
            pass_counter += 1
            matched = super().process(source)


class Document(Sequence):
    def __init__(self, fragments: List[Parser], identifier: str = 'Document') -> None:
        super().__init__(fragments, identifier=identifier)

    def process(self, source: Source) -> bool:
        matched = super().process(source)
    
    def report(self, target: TextIO) -> None:
        target.write(f'## {self.identifier:s}\n')
        target.write('\n')


