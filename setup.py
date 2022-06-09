import os
import json
import secrets

from helpers import (
    log,
    get_public_ip,
    CONFIG_DIR,
    CONFIG_FILE,
    get_config,
    DEPLOYMENT_TYPES,
    process_deployment_type,
)


def setup():
    if os.path.exists(CONFIG_DIR):
        log(
            "Config folder yet exists. To re-run the setup, delete your config dir",
            True,
            True,
        )
    setup_server()
    setup_deployment_type()
    log("Config saved")


def setup_deployment_type():
    print(
        "There are 5 different methods for deployment. The chosen method describes "
        "what is to be done when a call to the webhook is received. The methods are as "
        "follows:\n"
    )
    text = "\n".join([f"{key}: {value}" for key, value in DEPLOYMENT_TYPES.items()])
    print(text + "\n")
    _type = int(input("Please select a type, by entering its number: "))
    do_simple_pull, run_bash_script, run_python_function = process_deployment_type(
        _type
    )

    cfg = get_config()
    if do_simple_pull:
        cfg["repo_location"] = input(
            "Please provide the absolute folder path in which you want to pull. "
            "Important: The directory must already be a git repo, eg it must already "
            "be clonsed once: "
        )
    if run_bash_script:
        print(
            "Create your bash script, save it as `deploy.sh` in the root of this "
            "repository. It will be called when the webhook is called by Github"
        )
    if run_python_function:
        print(
            "Implement your python function in the function `custom_deploy` in `app.py`"
        )
    cfg["deployment_type"] = _type
    with open(CONFIG_FILE, "w") as file:
        json.dump(cfg, file)


def setup_server():
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
        "secret": secrets.token_hex(16),
    }
    os.mkdir(CONFIG_DIR)
    with open(CONFIG_FILE, "w") as file:
        json.dump(cfg, file)
    ip = get_public_ip()
    port = cfg["port"]
    secret = cfg["secret"]
    url = f"http://{ip}:{port}/deploy"
    print(
        f"\nUse the following info for your Github Webhook:\n Payload URL: {url}\n "
        f"Secret: {secret}\n"
    )


if __name__ == "__main__":
    setup()
