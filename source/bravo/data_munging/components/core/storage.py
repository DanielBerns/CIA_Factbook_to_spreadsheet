from pathlib import Path
from pathlib import Path

from components.core.helpers import (
    get_container,
    delete_container,
)


class Storage:
    def __init__(self, application: str, context: str, version: str) -> None:
        self._application: str = application
        self._context: str = context
        self._version: str = version
        base = Path('~', 'Apps', application, context, version)
        self._base: Path = get_container(base)
        self._dotenv: Path = Path(self.base, ".env")
        self._inputs: Path = get_container(Path(base, "inputs"))
        self._outputs: Path = get_container(Path(base, "outputs"))
        self._reports: Path = get_container(Path(base, "reports"))
        self._logs: Path = get_container(Path(base, "logs"))
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
    def inputs(self) -> Path:
        return self._inputs

    @property
    def outputs(self) -> Path:
        return self._outputs

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
