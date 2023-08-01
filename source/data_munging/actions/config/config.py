import os
from pathlib import Path
from actions.helpers import get_directory
import argparse

from typing import Dict

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

CONTEXT = "actions"
VERSION = "alpha"

def build_root(application: str) -> Path:
    root = Path('~', 'Data', application, CONTEXT, VERSION).expanduser()
    return root

def get_args() -> Dict[str, str]:
    """Construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    default_dotenv = '.env'
    parser.add_argument(
        "-d",
        "--dotenv",
        type=str,
        default=default_dotenv,
        help=f"default dotenv: {default_dotenv:s}",
    )
    args = vars(parser.parse_args())
    return args


def write_dotenv_example(
    dotenv_directory: Path,
    application_data: Path,
    application_reports: Path,
    application_logs: Path) -> None:
    """Write an example dotenv file, with expected keys.
    User may modify the values, and add remarks.
    See https://pypi.org/project/python-dotenv/
    """
    with open(dotenv_directory, "w") as target:
        target.write("SECRET_KEY=11111111\n")
        target.write("LOG_TO_STDOUT=YES\n")
        target.write(f"APPLICATION_DATA={str(application_data):s}\n")        
        target.write(f"APPLICATION_REPORTS={str(application_reports):s}\n")
        target.write(f"APPLICATION_LOGS={str(application_logs):s}\n")

def get_default_data_directory(application: str, version: str) -> Path:
    p = Path('~', 'Data', application, version).expanduser()
    return get_directory(p)


def get_default_reports_directory(application: str, version: str) -> Path:
    p = Path('~', 'Reports', application, version).expanduser()
    return get_directory(p)


def get_default_logs_directory(base: Path) -> Path:
    return get_directory(Path(base, "logs"))


def set_environment_variables(application: str, version: str) -> None:
    print("set_environment_variables start")
    application_data = get_default_data_directory(application, version)
    application_reports = get_default_reports_directory(application, version)
    application_logs = get_default_logs_directory(application_reports)
    args = get_args(application_data)
    print("set_environment_variables args", str(args))
    base = get_directory(Path(args["dotenv_path"]).resolve())
    print("set_environment_variables dotenv_path", str(base))
    dotenv_path = Path(base, ".env")
    if not dotenv_path.exists():
        write_dotenv_example(
            dotenv_path, 
            application_data, 
            application_reports,
            application_logs)
    load_dotenv(dotenv_path)
    print("set_environment_variables done")


set_environment_variables(CONTEXT, VERSION)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "11235813213455"
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    APPLICATION_DATA = os.environ.get("APPLICATION_DATA")    
    APPLICATION_REPORTS = os.environ.get("APPLICATION_REPORTS")
    APPLICATION_LOGS = os.environ.get("APPLICATION_LOGS")
    
