import os
from pathlib import Path
from actions.helpers import set_environment_variables

APPLICATION = 'CIA_World_Factbook-alpha'
DATA_DIRECTORY = Path('~', 'Data', 'CIA', 'factbook', 'factbook_html_zip').expanduser()

set_environment_variables(APPLICATION)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '11235813213455'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    REPORTS_DIRECTORY = os.environ.get('REPORTS_DIRECTORY')
