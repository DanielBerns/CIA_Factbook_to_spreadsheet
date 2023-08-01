from collections import defaultdict
from typing import Dict, Tuple, List, Generator

def collect_common_substrings(red: str, blue: str) -> Dict[str, List[Tuple[int, int]]]:
    collector = defaultdict(list)
    current = [0] * len(blue)
    index = [i for i in range(len(blue))]
    for dd in red:
        update = [cc + 1 if dd == tt else 0 for cc, tt in zip(current, blue)]
        for cc, uu, ii in zip(current, update, index):
            if cc > 1 and uu == 0:
                key = blue[ii - cc: ii]
                collector[key].append((ii - cc, ii))
        current[1:] = update[:-1]
        current[0] = 0
    return collector


def collected_strings(
    collector: Dict[str, List[Tuple[int, int]]]
) -> Generator[Tuple[str, int, int], None, None]:
    for key, positions in collector.items():
        for start, stop in positions:
            yield key, start, stop


def prepare_data(data: str, start: str, stop: str) -> str:
    return f"{start:s}{data:s}{stop:s}"


def compare(red: str, blue: str) -> Dict[str, List[Tuple[int, int]]]:
    start_red, stop_red = chr(1), chr(2)
    start_blue, stop_blue = chr(3), chr(4)
    
    collector = collect_common_substrings(
        prepare_data(red, start_red, stop_red),
        prepare_data(blue, start_blue, stop_blue)
    )
    
    return collector
