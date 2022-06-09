from flask import Flask

from helpers import get_config

app = Flask(__name__)
if __name__ == "__main__":
    """
    Run the flask app indefinitely
    """

    port = cfg = get_config('port')
    app.run(
        host="0.0.0.0",
        port=port,
    )
