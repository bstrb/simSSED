from flask import request

from simserialED.gui import app, template, NAVIGATION

NAVIGATION.append(
    {
        "caption": "Reset",
        "href": "/reset"
    }
)

@app.route("/reset", methods=['GET', 'POST'])
def reset():
    out = template("reset.html")
    if request.method == "POST":
        for key in request.cookies.keys():
            out.delete_cookie(key)
    return out
