import datetime
import json
from pathlib import Path


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


