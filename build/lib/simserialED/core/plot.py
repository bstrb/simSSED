# TODO make function
raw =simserialED.get_raw_data()
sims = raw["entry"]["data"]["simulations"]
datas = raw["entry"]["data"]["images"]
euler = raw["entry"]["data"]["euler_angles"]
from matplotlib import pyplot as plt
plt.figure()
plt.subplots_adjust(bottom=0.2)
plt.subplot(1, 2, 1)
sim = plt.imshow(sims[0])
text = plt.text(0, 0, "tmp")
plt.axis("off")
plt.subplot(1, 2, 2)
data = plt.imshow(datas[0])
plt.axis("off")

from orix.quaternion import Orientation
from orix.vector import Miller
p = simserialED.simulation.get_phase()
z = Miller(uvw=[0, 0, 1], phase=p)

plt.axis("off")

from matplotlib.widgets import Slider

s = Slider(plt.axes((0.1, 0.1, 0.8, 0.05)), "ind", 0, sims.shape[0])

def on_changed(val):
    ind = int(s.val)
    sim.set_data(sims[ind])
    data.set_data(datas[ind])
    o = Orientation.from_euler(euler[ind], degrees=True, symmetry=p.point_group)
    text.set_text(str((o * z).round()))

s.on_changed(on_changed)