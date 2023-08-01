from pathlib import Path
from pathlib import Path

from components.core.helpers import (
    get_container,
    delete_container,
)


class FileSystem:
    def __init__(self, application: str, context: str, version: str) -> None:
        self._application: str = application
        self._context: str = context
        self._version: str = version
        base = Path('~', 'info', application, context, version)
        self._base: Path = get_container(base)
        self._dotenv: Path = Path(base, ".env")
        self._data: Path = get_container(Path(base, "data"))
        self._results: Path = get_container(Path(base, "results"))
        self._reports: Path = get_container(Path(base, "reports"))
        self._logs: Path = get_container(Path(base, "logs")
        self._commands: Path = get_container(Path(base, "commands"))
        
    @property
    def application(self) -> str:
        return self._application

    @property
    def context(self) -> str:
        return self._context
    
    @property
    def version(self) -> str:
        return self._version
    
    @property
    def base(self) -> Path:
        return self._base

    @property
    def dotenv(self) -> Path:
        return self._dotenv

    @property
    def data(self) -> Path:
        return self._data

    @property
    def results(self) -> Path:
        return self._results

    @property
    def reports(self) -> Path:
        return self._reports

    @property
    def logs(self) -> Path:
        return self._logs

    @property
    def commands(self) -> Path:
        return self._commands

    def clear(self) -> None:
        if self.base.exists():
            delete_container(self.base)
