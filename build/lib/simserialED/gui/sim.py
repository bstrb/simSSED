from flask import request

from simserialED.core.simulation import get_simulations_with_params, phase_from_params, get_sample_reduced_fundamental

from simserialED.gui import app, template, NAVIGATION

NAVIGATION.append(
    {
        "caption": "Simulation",
        "href": "/simulate"
    }
)

@app.route("/simulate", methods=['GET', 'POST'])
def simulate():
    kwargs = {**request.cookies}
    kwargs["ready"] = kwargs.get("a") is not None
    kwargs["done"] = False

    if kwargs["ready"]:
        phase = phase_from_params(**kwargs)
        oris = get_sample_reduced_fundamental(float(kwargs["angres"]), point_group=phase.point_group)
        
        kwargs["spacegroup_full"] = phase.space_group.short_name
        kwargs["nsim"] = oris.size


    out = template("sim.html", **kwargs)
    if request.method == "POST" and kwargs["ready"]:
        sim = get_simulations_with_params(**kwargs)
        kwargs["done"] = True
    return out
