from collections import defaultdict

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

# def compare(source, target):
#     collector = defaultdict(list)
#     current = [0]*len(target)
#     index = [i for i in range(len(target))]
#     # print('  ', ', '.join((t for t in target)))
#     for k, s in enumerate(source):
#         update = [0]*len(target)
#         for c, i, t in zip(current, index, target):
#             if t == s:
#                 update[i] = c + 1
#             elif c:
#                 update[i] = 0
#                 if c > 1:
#                     key = target[i-c: i]
#                     collector[key].append((i-c, i))
#             else:
#                 pass
#         # print(s, update)
#         current[1:] = (u for u in update[:-1])
#     return collector


def show_collector(collector):
    for key, positions in collector.items():
        for start, stop in positions:
            yield key, start, stop

def main(red=None, blue=None):
    if red is None:
        red = 'uglz roses y fair bees'
    if blue is None:
        blue = 'uglz bees y fair roses'
    collector = compare(red, blue)

    for key, positions in collector.items():
        for start, stop in positions:
            print(start, stop, key)

if __name__ == '__main__':
   main()

