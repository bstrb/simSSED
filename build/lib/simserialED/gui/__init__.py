from flask import Flask, render_template, make_response, Response

from flask.cli import load_dotenv
from pathlib import Path
if not load_dotenv(Path(__file__).parent.parent / ".env"):
    raise ValueError("No .env found. Have you run simserialED.setup yet?")

app = Flask(__name__)
app.config.from_prefixed_env()

app.config["title"] = "SerialED simulation"

def template(template_name: str, **kwargs) -> Response:
    return make_response(render_template(template_name, **kwargs, **app.config))

NAVIGATION = []

from simserialED.gui import (
    setup,
    load,
    sim,
    reset
)

@app.route("/")
def index():
    return template("index.html", navigation=NAVIGATION)

