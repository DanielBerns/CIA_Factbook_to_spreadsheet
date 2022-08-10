from data_munging import substrings 
from data_munging import readers

from pathlib import Path

def main():
    this_file = Path('~', 'Data', 'CIA', 'factbook')
    text = readers.read_text_file(this_file)
    print(text)
    
if __name__ == '__main__':
    main()
