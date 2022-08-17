from actions import substrings, readers

from pathlib import Path

def main():
    this_file = Path('~', 
                     'Data', 
                     'CIA', 
                     'factbook', 
                     'factbook_html_zip',
                     'download.txt').expanduser()
    text = readers.api.slurp_text_file(this_file)
    print(text)
    
if __name__ == '__main__':
    main()
