class Source:
    def __init__(self, content: str, begin: int = 0, end: int = 1) -> None:
        assert 0 <= begin < len(content)
        assert 0 < end <= len(content)
        assert begin < end

        self._content: str = content
        self._begin: int = begin
        self._end: int = begin
    @property
    def content(self) -> str:
        return self._content[self.begin: self.end]
    
    
class Match:
    def __init__(self, prefix: str, alternative: Optional[str] = None) -> None:
        self._prefix: str = prefix
        self._alternative_prefix: str = alternative_prefix
        
    def update(self):
        
