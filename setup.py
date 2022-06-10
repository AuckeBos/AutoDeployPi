import os
import json
import secrets
import subprocess

from helpers import (
    log,
    get_public_ip,
    CONFIG_DIR,
    CONFIG_FILE,
    get_config,
    DEPLOYMENT_TYPES,
    process_deployment_type,
)


def setup_server():
    """
    Ask user for configuration of the server
    """
    cfg = {
        "server_port": input("On which port should the server listen? [default: 8855]:")
        or 8855,
        "secret": secrets.token_hex(16),
    }
    ip = get_public_ip()
    port = cfg["server_port"]
    secret = cfg["secret"]
    url = f"http://{ip}:{port}/deploy"
    print(
        f"\nUse the following info for your Github Webhook:\n Payload URL: {url}\n "
        f"Secret: {secret}\n"
    )
    _save_cfg(cfg)


def setup_deployment_type():
    cfg = get_config()
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
    if do_simple_pull:
        _dir = input(
            "Please provide the absolute folder path in which you want to pull. It "
            "must be empty: "
        )
        # Now run a `git init in the dir`

        if not os.path.exists(_dir):
            os.mkdir(_dir)
            print("Directory created")
        cmd = f"cd {_dir} && git init"
        subprocess.run(cmd, shell=True)
        cfg["repo_location"] = _dir

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
    _save_cfg(cfg)


def setup_supervisord():
    """
    Add a line to the crontab, which starts supervisord on reboot
    """
    supervisor_dir = _supervisor_dir()
    supervisord_loc = "$(poetry run which supervisord)"
    config_file = f"{supervisor_dir}/supervisord.conf"
    cron_line = f"@reboot {supervisord_loc} -c {config_file} 2>&1"
    user = _user()
    command = f'(crontab -u {user} -l; echo "{cron_line}") | crontab -u {user} -'
    current_cron = subprocess.check_output(f"crontab -u {user} -l", shell=True).decode(
        "utf-8"
    )
    # If the current config_file exists in the cron file, this command is already added
    # once dont't re-add it
    if config_file in current_cron:
        print("Not adding supervisord to cron, command yet exists in crontab")
    else:
        # First create the actual config file, based on the template
        _create_conf_file()
        print("Adding supervisor to cron, such that supervisord starts on reboot")
        # Then add the cron task
        os.system(command)
        print(
            "Cron added. Call the command as shown in your cron  manually now, "
            "or reboot to enable supervisord now"
        )

    print("Your current cron is as follows:")
    os.system(f"crontab -u {user} -l")
    print('')


def _supervisor_dir() -> str:
    """
    Get the supervisor dir
    """
    dir = os.path.dirname(os.path.realpath(__file__))
    config_dir = f"{dir}/supervisor"
    return config_dir


def _user() -> str:
    """
    Get the current user
    """
    return subprocess.check_output("whoami").strip().decode("utf-8")


def _create_conf_file():
    """
    Create a config file, based on the config template. The actual file has the <USER>
    and <PORT> variable replaced with the right values
    """
    port = (
        input(
            "Supervisord will run a local http server, to track its "
            "status. On which port should it run? [default: 9002]"
        )
        or 9002
    )

    # Load template
    dir = _supervisor_dir()
    template_file = f"{dir}/supervisord.conf.template"
    with open(template_file, "r") as f:
        template = f.read()

    # Replace variables
    content = template.replace("<USER>", _user()).replace("<PORT>", str(port))
    # Save
    conf_file = f"{dir}/supervisord.conf"
    with open(conf_file, "w") as f:
        f.write(content)


def _save_cfg(cfg):
    with open(CONFIG_FILE, "w") as file:
        json.dump(cfg, file)


def setup_all():
    """
    Run the complete setup
    """
    if os.path.exists(CONFIG_DIR):
        log(
            "Config folder yet exists. To re-run the setup, delete your config dir",
            True,
            True,
        )
    print(
        "Important: To receive webhook calls from github, a Flask server will be "
        "running permanently on your machine. This server needs to be publicly "
        "available. You should either open up a port on your router, or use some "
        "tunneling service, for example ngrok"
    )
    input("Press enter to key to continue...")
    print("")

    print(
        "Important: Make sure crontab is installed, and a crontab exists for your user."
    )
    input("Press enter to key to continue...")

    os.mkdir(CONFIG_DIR)
    setup_server()
    setup_deployment_type()
    setup_supervisord()
    log("Config saved")


if __name__ == "__main__":
    setup_all()
