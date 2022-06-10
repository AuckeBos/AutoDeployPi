import json
import os
import subprocess

from flask import Flask, request

from helpers import get_config, log

app = Flask(__name__)


@app.route("/deploy", methods=["POST"])
def deploy():
    """
    Run the deploy. Called by Github
    """
    payload = json.loads(request.data.decode())
    log(f"Received {payload}")

    try:
        url = payload["repository"]["html_url"]
        deployment_config = get_config("deployments")
        if url not in deployment_config:
            log(f"{url} not configered as auto-deploy server", True, True)
        else:
            script = deployment_config[url]
            cmd = f"./scripts/{script}.sh"
            log(f"Running {cmd}")
            subprocess.run(cmd, shell=True)
        log("Done!")
        return "OK", 200
    except Exception as e:
        log(f"An error occurred: {e}", True, True)


if __name__ == "__main__":
    """
    Run the flask app indefinitely
    """

    port = cfg = get_config("server_port")
    app.run(
        host="0.0.0.0",
        port=port,
    )
