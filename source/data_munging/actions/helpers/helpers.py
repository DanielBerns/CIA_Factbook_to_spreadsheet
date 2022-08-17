import argparse
import datetime
import json
from pathlib import Path
from typing import Dict, Iterator

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv


def get_timestamp():
    now = datetime.datetime.now()
    timestamp = ''.join([f'{now.year:4d}{now.month:02d}',
                         f'{now.day:02d}{now.hour:02d}',
                         f'{now.minute:02d}'])
    return timestamp


def save_metadata(metadata_path, metadata):
    with open(metadata_path, 'w') as target:
        json.dump(metadata, target)


def load_metadata(metadata_path):
    metadata = None
    with open(metadata_path, 'r') as source:
        metadata = json.load(source)
    return metadata


def get_directory(base: Path):
    directory = Path(base).expanduser()
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    return directory


def get_args(dotenv_path: str) -> Dict[str, str]:
    """Construct the argument parser and parse the arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dotenv_path", 
                        type=str,  default=dotenv_path,
                        help="path where dotenv lives")
    args = vars(parser.parse_args())
    return args


def default_reports_directory(application: str) -> Path:
    path = Path('~', 'Reports', 'data_munging', application)
    return get_directory(path)


def write_dotenv_example(
    dotenv_directory: Path, 
    reports_directory: Path) -> None:
    """Write an example dotenv file, with expected keys.
       User may modify the values, and add remarks.
       See https://pypi.org/project/python-dotenv/
    """
    with open(dotenv_directory, 'w') as target:
        target.write("SECRET_KEY=11111111\n")
        target.write("LOG_TO_STDOUT=YES\n")        
        target.write(f"REPORTS_DIRECTORY={str(reports_directory):s}\n\n")    


def set_environment_variables(application: str) -> None:
    print('set_environment_variables start')
    args = get_args(str(Path('~', 'Data', application).expanduser()))
    print('set_environment_variables args', str(args))
    base = get_directory(Path(args['dotenv_path']).resolve())
    print('set_environment_variables dotenv_path', str(base))
    dotenv_path = Path(base, '.env')
    reports_directory = default_reports_directory(application)
    if not dotenv_path.exists():
        write_dotenv_example(dotenv_path, reports_directory)
    load_dotenv(dotenv_path)
    print('set_environment_variables done')


# def write_text(
#     text_directory: Path,
#     string_iterator: Iterator[str]
#     ) -> None:
#     with open(dotenv_directory, 'w') as target:
#         for string in string_iterator:
#             target.write(f'{string:s}\n')
