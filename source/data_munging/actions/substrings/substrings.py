from collections import defaultdict
from typing import Dict, Tuple

def compare(source, target):
    collector = defaultdict(list)
    current = [0]*len(target)
    index = [i for i in range(len(target))]
    for k, s in enumerate(source):
        update = [c + 1 if t == s else 0 for c, i, t in zip(current, index, target)]
        for c, u, i in zip(current, update, index):
            if u:
                continue
            if c > 1:
                key = target[i-c: i]
                collector[key].append((i-c, i))
        current[1:] = (u for u in update[:-1])
    return collector


def common_substrings(collector: Dict[str, Tuple[int, int]]):
    for key, positions in collector.items():
        for start, stop in positions:
            yield key, start, stop


if __name__ == '__main__':
   main()

