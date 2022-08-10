from pathlib import Path 

def read_text_file(text_file: Path) -> str:
    text = None
    with open(text_file, 'r') as source:
        text = source.read()
    return text
