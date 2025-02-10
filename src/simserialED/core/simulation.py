from pathlib import Path

from orix.crystal_map import Phase
from orix.sampling import get_sample_reduced_fundamental
from diffsims.generators.simulation_generator import SimulationGenerator
from diffsims.simulations import Simulation2D

from diffpy import structure as diffpy

def get_phase() -> Phase:
    # https://www.rcsb.org/structure/7SKW
    lattice = diffpy.Lattice(
        a=26.42,
        b=30.72,
        c=33.01,
        alpha=88.319,
        beta=109.095,
        gamma=112.075
    )
    

    atoms = [diffpy.Atom("C", [0, 0, 0])]
    structure = diffpy.Structure(atoms, lattice)
    phase = Phase("Simple lysozyme", space_group=1, structure=structure)
    return phase

def phase_from_params(a: float, b: float, c: float, alpha: float, beta: float, gamma: float, spacegroup: int, **kwargs) -> Phase:
    lattice = diffpy.Lattice(
        a=float(a),
        b=float(b),
        c=float(c),
        alpha=float(alpha),
        beta=float(beta),
        gamma=float(gamma),
    )
    
    atoms = [diffpy.Atom("C", [0, 0, 0])]
    structure = diffpy.Structure(atoms, lattice)
    phase = Phase("Phase name", space_group=int(spacegroup), structure=structure)
    return phase

def get_simulations() -> Simulation2D:
    """lysozyme, but primitive (easier intensity calculations)"""
    gen = SimulationGenerator(accelerating_voltage=300, precession_angle=0)
    
    phase = get_phase()

    oris = get_sample_reduced_fundamental(1, point_group=phase.point_group)
    return gen.calculate_diffraction2d(phase, oris, with_direct_beam=False, reciprocal_radius=1.4*0.7)

def get_simulations_with_params(a: float, b: float, c: float, alpha: float, beta: float, gamma: float, spacegroup: int, kv: float, angres: float, **kwargs) -> Simulation2D:
    gen = SimulationGenerator(accelerating_voltage=float(kv))
    
    phase = phase_from_params(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma, spacegroup=spacegroup)

    oris = get_sample_reduced_fundamental(float(angres), point_group=phase.point_group)
    return gen.calculate_diffraction2d(phase, oris, with_direct_beam=False)


def get_simulations_from_cif(cif_file: Path) -> Simulation2D:
    gen = SimulationGenerator(accelerating_voltage=300, precession_angle=0)
    
    phase = Phase.from_cif(Path(__file__).parent.parent.parent / "data" / "lysozyme.cif")
    print(phase, phase.structure.lattice, len(phase.structure))

    oris = get_sample_reduced_fundamental(10, point_group=phase.point_group)
    return gen.calculate_diffraction2d(phase, oris, with_direct_beam=False, reciprocal_radius=1.4*0.7)