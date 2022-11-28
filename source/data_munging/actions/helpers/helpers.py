import argparse
import datetime
import json
from pathlib import Path
from typing import Dict, List, Iterator, Union



def get_timestamp():
    now = datetime.datetime.now()
    timestamp = "".join(
        [
            f"{now.year:4d}{now.month:02d}",
            f"{now.day:02d}{now.hour:02d}",
            f"{now.minute:02d}",
            f"{now.second:02d}",
        ]
    )
    return timestamp


def save_json(data_json: Path, data: Union[Dict, List]):
    with open(data_json, "w") as target:
        json.dump(data, target)


def load_json(data_json: Path) -> Dict:
    data = None
    with open(data_json, "r") as source:
        data = json.load(source)
    return {'array': data} if is_instance(data, List) else data


def get_directory(base: Path):
    directory = Path(base).expanduser()
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    return directory




# def write_text(
#     text_directory: Path,
#     string_iterator: Iterator[str]
#     ) -> None:
#     with open(dotenv_directory, 'w') as target:
#         for string in string_iterator:
#             target.write(f'{string:s}\n')
