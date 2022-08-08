def compare(source, target):
    collector = list()
    current = [0]*len(target)
    index = [i for i in range(len(target))]
    print('  ', ', '.join((t for t in target)))
    for k, s in enumerate(source):
        update = [0]*len(target)
        for c, i, t in zip(current, index, target):
            if t == s:
                update[i] = c + 1
            elif c:
                update[i] = 0
                if c > 1:
                    collector.append((i-c, i, target[i-c: i]))
            else:
                pass
        print(s, update)
        current[1:] = (u for u in update[:-1])
    return collector

def extract(target, substring_length):
    substring = []
    for t, r, b in zip(target, substring_length[:-1], substring_length[1:]):
        if r < b:
            substring.append(t)
        else:
            if substring:
                yield ''.join(substring)
                substring = []


def main(red=None, blue=None):
    if red is None:
        red = 'uglz roses y fair bees'
    if blue is None:
        blue = 'uglz bees y fair roses'
    collector = compare(red, blue)
    print(red)
    print(blue)
    for start, stop, substring in collector:
        print(start, stop, substring)

if __name__ == '__main__':
   main()

