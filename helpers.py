import datetime
import json
import os
import requests

CONFIG_DIR = os.path.dirname(__file__) + "/config"
CONFIG_FILE = f"{CONFIG_DIR}/cfg.json"

DEPLOYMENT_TYPES = {
    1: "Simple run `git pull repo_url` in a specific directory",
    2: "Run a custom bash script when the webhook is called",
    3: "Run a custom python function when the webhook is called",
    4: "1 and 2",
    5: "1 and 3",
}


def log(msg, error=False, fatal=False):
    """
    Helper function to log any data to stdout
    """
    typestring = "E" if error else "I"
    print(
        f'[{typestring}] [{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] - '
        f"{msg}"
    )
    if fatal:
        exit()


def setup_needed() -> bool:
    """
    Check whether the setup has been ran. If not, return True
    """
    return not os.path.exists(CONFIG_DIR)


def get_config(key=None):
    """
    Load config json file. If key is provided, return only that value. Otherwise the
    complete dict
    """
    if setup_needed():
        log("Please run the setup script: python setup.py", True, True)

    with open(CONFIG_FILE) as file:
        cfg = json.load(file)
        if key is not None:
            return cfg[key]
        return cfg


def get_public_ip():
    """
    Get the current public ip address
    """
    return requests.get("http://ipinfo.io/json").json()["ip"]


def process_deployment_type(_type: int):
    """
    Parse the deployment type
    :param type:  The type
    :return: Tuple[bool,bool,bool]
    Indiciating whether to:
        - Do a simple git pull
        - Run the bash script
        - Run the python function
    """
    do_simple_pull = _type in (1, 4, 5)
    run_bash_script = _type in (2, 5)
    run_python_function = _type in (3, 5)

    return do_simple_pull, run_bash_script, run_python_function
