import json
from pathlib import Path

from flask import request, flash
import h5py

from simserialED.gui import app, template, NAVIGATION

NAVIGATION.append(
    {
        "caption": "Load file",
        "href": "/load"
    }
)


@app.route("/load", methods=['GET', 'POST'])
def load():
    file = request.cookies.get("hdf5_file", "No file loaded")
    if request.method == "POST":
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename
        root = Tk()
        root.withdraw()
        # ensure the file dialog pops to the top window
        root.wm_attributes('-topmost', 1)
        file = askopenfilename(parent=root)
    try:
        data = open_hdf5(file)
    except AssertionError as e:
        content = ""
        flash(str(e))
    else:
        content = serialize_hdf5(data)
        data.close()

    res = template("load.html", filename=file, content=content)
    if content:
        res.set_cookie("hdf5_file", file)
    return res


def open_hdf5(path: str | Path) -> h5py.File:
    if isinstance(path, str):
        path = Path(path)
    assert path.suffix in [".h5", ".hdf5"], "File must be HDF5 format"
    return h5py.File(path, "r+")

def _group_to_dict(d: dict[str, h5py.Group | h5py.Dataset]) -> dict:
    d = {key: val for key, val in d.items()} # Don't touch the file
    for key, val in d.items():
        if isinstance(val, h5py.Group):
            d[key] = _group_to_dict(d[key])
        else:
            d[key] = str(val)
    return d

def serialize_hdf5(file: h5py.File) -> str:
    d = {key: val for key, val in file.items()}
    d = _group_to_dict(d)
    return json.dumps(d, indent=4)
