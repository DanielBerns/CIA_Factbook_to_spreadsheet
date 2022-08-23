import os
from pathlib import Path
from actions.helpers import set_environment_variables

APPLICATION = "CIA_World_Factbook_Albatros"
VERSION = "alpha"
WORLD_FACTBOOK_RAW_DATA = Path("~", "Data", "CIA", "factbook", "factbook_html_zip").expanduser()


set_environment_variables(APPLICATION, VERSION)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "11235813213455"
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    APPLICATION_REPORTS = os.environ.get("APPLICATION_REPORTS")
    APPLICATION_DATA = os.environ.get("APPLICATION_DATA")    
