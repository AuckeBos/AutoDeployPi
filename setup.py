import os
import json

CONFIG_DIR = os.path.dirname(__file__) + "/config"
CONFIG_FILE = f"{CONFIG_DIR}/cfg.json"


def setup():
    if os.path.exists(CONFIG_DIR):
        print("Config folder yet exists. To re-run the setup, delete your config dir")
        exit()
    print(
        "Important: To receive webhook calls from github, a Flask server will be "
        "running permanently on your machine. This server needs to be publically "
        "available. You should either open up a port on your router, or use some "
        "tunneling service, for example ngrok"
    )
    input("Press enter to key to continue...")

    cfg = {
        "port": input("On which port should the server listen? [default: 8855]:")
        or 8855,
    }
    os.mkdir(CONFIG_DIR)
    with open(CONFIG_FILE, "x") as file:
        json.dump(cfg, file)


if __name__ == "__main__":
    setup()
