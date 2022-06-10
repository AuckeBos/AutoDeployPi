import datetime
import json
import os
import requests

CONFIG_DIR = os.path.dirname(__file__) + "/config"
CONFIG_FILE = f"{CONFIG_DIR}/cfg.json"

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


def save_config(cfg):
    """
    Save the config dir
    """
    with open(CONFIG_FILE, "w") as file:
        json.dump(cfg, file)


def get_public_ip():
    """
    Get the current public ip address
    """
    return requests.get("http://ipinfo.io/json").json()["ip"]
