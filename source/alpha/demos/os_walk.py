import os
from pathlib import Path 
from typing import Tuple

import pdb

def demo_os_walk(directory: Path) -> Tuple[Path, Path]:
    pdb.set_trace()
    for root, dirs, files in os.walk(directory, topdown=False):
        for a_file in files:
            yield root, a_file
        for a_dir in dirs:
            yield root, a_dir


if __name__ == '__main__':
    this_directory = Path(
        '~', 'Data', 'CIA', 'factbook', 'factbook_html_zip'
        ).expanduser()
    for number, (root, leaf) in enumerate(demo_os_walk(this_directory)):
        print(number, '-', str(root), '-', str(type(leaf)), '-', str(leaf))
              
