import os

from helpers import (
    get_config,
    save_config,
    log,
    get_public_ip,
)


def add_repo():
    """
    Add a repository to auto-deploy
    :return:
    """
    cfg = get_config()

    repo_url = input(
        "What is the url of the homepage of repo you want to auto-deploy? "
    )
    script = input(
        "Create your bash script, save it in the `scripts` folder of this repo. "
        "What is the filename? "
    )
    script = script.replace(".sh", "")
    path = f"./scripts/{script}.sh"
    if not os.path.exists(path):
        log("Script not found, please create it first", True, True)
    os.chmod(path, 777)

    current_deployment_config = cfg["deployments"]
    current_deployment_config[repo_url] = script

    save_config(cfg)

    ip = get_public_ip()
    port = cfg["server_port"]
    secret = cfg["secret"]
    url = f"http://{ip}:{port}/deploy"
    print(
        f"\n"
        f"Go to {repo_url}/settings/hook/new"
        f"\nEnter the following info:"
        f"\n Payload URL: {url}"
        f"\n Content type: apication/json"
        f"\n Secret: {secret}"
        f"\n Which events would you like to trigger this webhook?: Just push the event."
        f"\n Active: Checked"
        "\nAnd add the webhook"
        "\n"
    )

    input(
        "===IMPORTANT===\n"
        f"Port {port} should be publicly available"
        f"\nPress "
        f"enter to continue..."
    )

    print("Auto deployment saved")


if __name__ == "__main__":
    add_repo()
