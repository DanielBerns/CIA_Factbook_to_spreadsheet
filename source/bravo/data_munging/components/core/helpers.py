import datetime
import json
from pathlib import Path
from shutil import rmtree
from typing import Dict, List, Union


def get_container(base: Path) -> Path:
    container = Path(base).expanduser()
    container.mkdir(mode=0o700, parents=True, exist_ok=True)
    return container


def delete_container(base: Path) -> None:
    rmtree(base)
    
    
def get_timestamp() -> str:
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
