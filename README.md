# AutoDeployPi

This repo contains a small python program, that allows your pi (or any other linux 
server), to automatically pull any changes from git, whenever you push to a repo on 
Github.

## Deployment flow
Your server listens for any webhook calls by the repo you've configured it to 
listen to. Whenever the webhook is called by git, your server calls a 
manually-defined shell script, in which you define your deployment procedure. In 
the simplest case, the procedure could simply be `cd {directory} && git pull {url}`.

## Setup
To setup the server, run the following steps:
1. Poetry is used as a dependency manager. Make sure [Poetry is installed](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions).
2. Install the dependencies in a new venv: `poetry install`.
3. Run the setup script: `poetry run python setup.py`, this will ask you for the 
   one-time setup information:
   1. It asks you to make sure your server is publicly available on the port of 
      your choice. Flask will run on this port.
   2. Cron must be installed, as it is used to startup [supervisord](http://supervisord.org/) on boot.
        Supervisord is a program that can supervise any task, handles loging, and 
      restarts a service when it has crashed. It is used to ensure that your flask 
      server will always keep running.
   3. It asks you for the port you will be running the flask server on
   4. It asks you for a secret. It is used to verify github requests (todo).
   5. It adds a cronjob to start supervisord on boot
   6. It creates a supervisord.conf file based on your user and port.
4. The server is ready to be used. Start it by copying the cron command that is 
   logged to the terminal during setup, or simply reboot your system (as this cron 
   command is ran on reboot).
5. To use the server for a specific repo, run `poetry run python add_repo.py` to add 
   a repo for auto deployment. It asks the needed info:
   1. It asks for the url (of the main-page) of the repo you want to auto deploy
   2. It asks for the name of the .sh script you want to call whenever the webhook is 
      called by git. Make sure this script is added in the `scripts` folder, and is a 
      bash script.
   3. It tells you how to configure the Github repo to call the webhook of your flask 
      server
6. Ready! Whenever anything is pushed to your repo, Github will call your server, 
   which will run your custom bash script. To add more repos, simply add one using 
   `poetry run python add_repo.py`.

