import json
import os
import subprocess

from flask import Flask, request

from helpers import get_config, process_deployment_type, log

app = Flask(__name__)


@app.route("/deploy", methods=["POST"])
def deploy():
    """
    Run the deploy. Called by Github
    """
    deployment_type = get_config("deployment_type")
    simple_pull, bash_script, python_function = process_deployment_type(deployment_type)
    if simple_pull:
        payload = json.loads(request.data.decode())
        url = payload["repository"]["clone_url"]
        do_simple_pull(url)
    if bash_script:
        run_bash_script()
    if python_function:
        run_python_function()
    return "OK", 200


def do_simple_pull(url: str):
    """
    Run the git pull command
    :param url:  The url of the repo to pull (the same repo as the one that called
    the webhook)
    """
    path = get_config("repo_location")

    if not os.path.exists(path):
        log(
            f"Not running git pull, please make sure the dir {path} exists.",
            True,
        )
    else:
        cmd = f"cd {path} && git pull {url}"
        log(f"Running `{cmd}`")
        subprocess.run(cmd, shell=True)


def run_bash_script():
    """
    Run the bash script, if it exists
    """
    if not os.path.exists("./bash.sh"):
        log(
            "Not running bash script, as it doesn't exist. Please create a file "
            "bash.sh in the root of this repo",
            True,
        )
    else:
        cmd = f"./bash.sh"
        log(f"Running `{cmd}`")
        subprocess.run(cmd, shell=True)


def run_python_function():
    """
    Run the python function
    """
    log("Running the `deploy` function")
    custom_deploy()


def custom_deploy():
    """
    Implement this function yourself, if you want to deploy by using this function
    """
    log("Please implement custom_deploy", True)


if __name__ == "__main__":
    """
    Run the flask app indefinitely
    """

    port = cfg = get_config("port")
    app.run(
        host="0.0.0.0",
        port=port,
    )
