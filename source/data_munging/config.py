import os
from pathlib import Path
from actions.helpers.api import set_environment_variables

APPLICATION = 'CIA_World_Factbook-alpha'

set_environment_variables(APPLICATION)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '11235813213455'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    OUTPUT_DIRECTORY = os.environ.get('OUTPUT_DIRECTORY')
