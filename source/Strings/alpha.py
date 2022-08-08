from collections import defaultdict


def phrase2str(phrase):
    value = ':'.join([f'{p:>2s}' for p in phrase])
    return '  :' + value + ':  '


def index2str(index_target):
    value = ':'.join([f'{i:>2d}' for i in index_target])
    return '  :' + value + ':  '


def value2str(value):
    return ':'.join([f'{v:>2d}' for v in value])

def compare(source, target):
    s = source[0]
    current = [1 if t == s else 0 for t in target]
    for s in source[1:]:
        previous = [c for c in current]
        current = 
def compare(source, target):
    patterns = list()
    index_source = [k for k in range(len(source))]
    index_target = [k for k in range(len(target))]
    current = [0]*(len(target) + 2)
    s = source[0]
    current[1:-1] = [1 if t == s else 0 for t in target]
    r = -1
    for i, c in zip(index_target, current[1:-1]):
        if c:
           patterns.append((c,r+2,i+1)) 
    for r, s in enumerate(source[1:]):
        previous = [c for c in current]
        current[1:-1] = [p + 1 if t == s else 0 for t, p in zip(target, previous[0:-2])]
        for i, c in zip(index_target, current[1:-1]):
            if c:
               patterns.append((c,r+2,i+1)) 
    return patterns, previous, current

def get_longest_patterns(patterns):
    patterns_length = defaultdict(list)
    longest_patterns = list()
    for c, r, i in sorted(patterns):
        patterns_length[i-c].append(i)
    for start, end_values in patterns_length.items():
        end_max = max(end_values)
        this_pattern = blue[start:end_max]
        longest_patterns.append(this_pattern)
    return longest_patterns

def process_red_and_blue(red, blue):
    patterns, previous, current = compare(red, blue)
    longest_patterns = get_longest_patterns(patterns)
    print(red)
    print(blue)
    print('-'*80)    
    print('## Patterns')
    for c, r, i in patterns:
        print(blue[i-c:i])
    print('-'*80)
    print('## Longest patterns')
    for p in longest_patterns:
        if len(p) > 2:
            print('  ', p)
    print('*'*80)

if __name__ == '__main__':
    red = 'one ugly thing and two fair ones. What do you want from me?'
    blue = 'two fair things and one ugly. I want from me!'
    process_red_and_blue(red, blue)
