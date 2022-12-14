import os
from pathlib import Path
from actions.helpers import get_directory

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

APPLICATION = "CIA_World_Factbook_Albatros"
VERSION = "alpha"
WORLD_FACTBOOK_RAW_DATA = Path("~", "Data", "CIA", "factbook", "factbook_html_zip").expanduser()


def get_args(application_data: str) -> Dict[str, str]:
    """Construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dotenv_path",
        type=str,
        default=application_data,
        help="path where dotenv lives",
    )
    args = vars(parser.parse_args())
    return args


def write_dotenv_example(
    dotenv_directory: Path,
    application_data: Path,
    application_reports: Path) -> None:
    """Write an example dotenv file, with expected keys.
    User may modify the values, and add remarks.
    See https://pypi.org/project/python-dotenv/
    """
    with open(dotenv_directory, "w") as target:
        target.write("SECRET_KEY=11111111\n")
        target.write("LOG_TO_STDOUT=YES\n")
        target.write(f"APPLICATION_DATA={str(application_data):s}\n")        
        target.write(f"APPLICATION_REPORTS={str(application_reports):s}\n")


def default_data_directory(application: str, version: str) -> Path:
    p = Path('~', 'Data', application, version).expanduser()
    return get_directory(p)


def default_reports_directory(application: str, version: str) -> Path:
    p = Path('~', 'Reports', application, version).expanduser()
    return get_directory(p)


def get_default_logs_directory(base: Path) -> Path:
    return get_directory(Path(base, "logs"))


def set_environment_variables(application: str, version: str) -> None:
    print("set_environment_variables start")
    application_data = get_default_data_directory(application, version))
    application_reports = get_default_reports_directory(application, version))
    application_logs = get_default_logs_directory(application_reports)
    args = get_args(application_data)
    print("set_environment_variables args", str(args))
    base = get_directory(Path(args["dotenv_path"]).resolve())
    print("set_environment_variables dotenv_path", str(base))
    dotenv_path = Path(base, ".env")
    if not dotenv_path.exists():
        write_dotenv_example(dotenv_path, application_data, application_reports)
    load_dotenv(dotenv_path)
    print("set_environment_variables done")


set_environment_variables(APPLICATION, VERSION)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "11235813213455"
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    APPLICATION_REPORTS = os.environ.get("APPLICATION_REPORTS")
    APPLICATION_DATA = os.environ.get("APPLICATION_DATA")    
