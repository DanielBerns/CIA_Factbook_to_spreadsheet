import argparse
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

def get_args(datapath: str) -> Dict[str, str]:
    """Construct the argument parser and parse the arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datapath", 
                        type=str,  default=datapath,
                        help="data path")
    args = vars(parser.parse_args())
    return args

def set_environment_variables(instance: str) -> None:
    print('set_environment_variables start')
    args = get_args(str(Path('~', 'Data', instance).expanduser()))
    datapath = Path(args['datapath']).resolve()
    print('set_environment_variables datapath', str(datapath))
    datapath.mkdir(mode=0o700, parents=True, exist_ok=True)
    dotenv_abspath = Path(datapath, '.env')
    load_dotenv(dotenv_abspath)
    print('set_environment_variables done')
    
if __name__ == '__main__':
   
