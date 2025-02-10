from flask import request

from simserialED.gui import app, template, NAVIGATION

NAVIGATION.append(
    {
        "caption": "Simulation parameters",
        "href": "/setup"
    }
)

@app.route("/setup", methods=['GET', 'POST'])
def setup():
    out = template("setup.html")
    if request.method == "POST":
        for key, val in request.form.items():
            out.set_cookie(key, val)
    return out
