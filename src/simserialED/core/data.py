from pathlib import Path
import json

import hyperspy.api as hs
import pyxem as pxm
from dask import array as da
import h5py
import numpy as cp
import numpy as np

def get_raw_data(filepath: Path = None) -> h5py.File:
    if filepath is None:    
        filepath = list(Path(__file__).parent.parent.parent.parent.parent.glob("data/*"))[0]
    data = h5py.File(filepath, "r+")
    return data

def get_filtered_data(filepath: Path = None) -> pxm.signals.ElectronDiffraction2D:
    data = get_raw_data(filepath)
    array = da.array(data["entry"]["data"]["images"])
    array = array[::30]
    array = array.rechunk((64, -1, -1))
    f = np.max(np.abs(array), axis=(1, 2)) > 150
    array = array[f]
    array.compute()
    array.compute_chunk_sizes()
    signal = pxm.signals.LazyElectronDiffraction2D(array)
    return signal

def get_data(filepath: Path = None) -> pxm.signals.ElectronDiffraction2D:
    data = get_raw_data(filepath)
    array = da.array(data["entry"]["data"]["images"])
    signal = pxm.signals.ElectronDiffraction2D(array, chunksize=(100, -1, -1)).as_lazy()
    return signal

def get_data_gpu(filepath: Path = None) -> pxm.signals.ElectronDiffraction2D:
    data = get_raw_data(filepath)
    array = da.array(data["entry"]["data"]["images"])
    array = array.map_blocks(cp.asarray)
    signal = pxm.signals.ElectronDiffraction2D(array, chunksize=(100, -1, -1)).as_lazy()
    return signal

def get_test_data() -> pxm.signals.ElectronDiffraction2D:
    filepath = Path(__file__).parent.parent.parent / "data" / "test.hspy"
    signal = hs.load(filepath, lazy=False)
    signal.set_diffraction_calibration(1 / 3.9 / 183)
    return signal

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
