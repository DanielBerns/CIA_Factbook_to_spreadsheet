import os
from pathlib import Path
import argparse

from typing import Dict

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

DEFAULT_LOGGING_LEVEL = "WARNING"
DEFAULT_LOG2STDOUT = "NO"

def get_args() -> Dict[str, str]:
    """Construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--loglevel",
        type=str,
        default=DEFAULT_LOGGING_LEVEL,
        help=f"default log level: {DEFAULT_LOGGING_LEVEL:s}",
    )
    parser.add_argument(
        "--log2stdout",
        type=str,
        default="NO",
        help=f"default log to stdout: {DEFAULT_LOG2STDOUT:s}",
    )
    args = vars(parser.parse_args())
    return args


class Configuration:

    DEFAULT_SECRET_KEY = "11235813213455"    
    
    def __init__(self, dotenv: Path):
        if not dotenv.exists():
            self.write_dotenv_example(dotenv)
        load_dotenv(dotenv)
        self._secret_key: str = os.environ.get("SECRET_KEY") or \
            Configuration.DEFAULT_SECRET_KEY

    @property
    def secret_key(self) -> str:
        return self._secret_key
    
    def write_dotenv_example(self, dotenv: Path) -> None:
        """Write an example dotenv file, with expected keys.
        User may modify the values, and add remarks.
        See https://pypi.org/project/python-dotenv/
        """
        with open(dotenv, "w") as target:
            target.write(f"SECRET_KEY={DEFAULT_SECRET_KEY:s}\n")
