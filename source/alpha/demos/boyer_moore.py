# https://gist.github.com/dbrgn/1154006

def find_last_occurrence(pattern: str, letter: str) -> int:
    assert len(letter) == 1
    k = 0
    for k, p in enumerate(pattern[::-1]):
        if p == letter:
            return len(pattern) - k - 1
    return -1


class LastOccurrence:
    """Last occurrence functor."""

    def __init__(self, pattern: str, alphabet: str) -> None:
        """Generate a dictionary with the last occurrence of each alphabet
        letter inside the pattern.
        """
        self.occurrences = dict()
        for letter in alphabet:
            self.occurrences[letter] = find_last_occurrence(pattern, letter)

    def __call__(self, letter):
        """Return last position of the specified letter inside the pattern.
        Return -1 if letter not found in pattern."""
        return self.occurrences[letter]


def boyer_moore_match(text, pattern):
    """Find occurrence of pattern in text."""
    alphabet = set(text)
    last = LastOccurrence(pattern, alphabet)
    m = len(pattern)
    n = len(text)
    i = m - 1  # text index
    j = m - 1  # pattern index
    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        else:
            l = last(text[i])
            i = i + m - min(j, 1+l)
            j = m - 1 
    return -1

def main():        
    def show_match(text, pattern):
        print('Text:  ', text)
        p = boyer_moore_match(text, pattern)
        print('Match: ', '.'*p, pattern)

    text = 'abacaabadcabacabaabb'
    pattern = 'abacab'
    show_match(text, pattern)

    text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.'
    pattern = 'dolor'
    show_match(text, pattern)
    show_match(text, pattern + 'e') 


def demo_find_last_occurrence():
    pattern = '123456'
    characters = '123456'
    for k, c in enumerate(characters):
        print(k, c, find_last_occurrence(pattern, c))   
    fails = 'asdf'
    for k, c in enumerate(fails):
        print(k, c, find_last_occurrence(pattern, c))    
        
if __name__ == '__main__':
    main()
