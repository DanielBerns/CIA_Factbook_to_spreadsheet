import os
import argparse
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

# https://pypi.org/project/python-dotenv/

def get_args(datapath: str) -> Dict[str, str]:
    """Construct the argument parser and parse the arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datapath", 
                        type=str,  default=datapath,
                        help="data path")
    args = vars(parser.parse_args())
    return args


def write_dotenv_example(dotenv_abspath: Path) -> None:
    with open(dotenv_abspath, 'w') as target:
        target.write("SECRET_KEY=11111111\n")
        target.write("LOG_TO_STDOUT=YES\n")        
        target.write("DATA_DIRECTORY=~/Data/data_munging\n\n")    


def set_environment_variables(application: str) -> None:
    print('set_environment_variables start')
    args = get_args(str(Path('~', 'Data', application).expanduser()))
    datapath = Path(args['datapath']).resolve()
    print('set_environment_variables datapath', str(datapath))
    datapath.mkdir(mode=0o700, parents=True, exist_ok=True)
    dotenv_abspath = Path(datapath, '.env')
    if not dotenv_abspath.exists():
        write_dotenv_example(dotenv_abspath)
    load_dotenv(dotenv_abspath)
    print('set_environment_variables done')


            
APPLICATION = 'data_munging'
set_environment_variables(APPLICATION)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '11235813213455'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    DATA_DIRECTORY = os.environ.get('DATA_DIRECTORY') or str(Path('~', 'Data', APPLICATION).expanduser())

