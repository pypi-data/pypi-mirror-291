import pytest

pytest.skip(allow_module_level=True)
import pathlib

from ase.calculators.gaussian import Gaussian
from ase.calculators.gaussian import GaussianOptimizer
import ase.io
from numpy.linalg import norm

atoms = ase.io.read("FePc_med_spin_NHO_on_Fe_parallel_3.traj")

label = "Gaussian"

calc = Gaussian(
    command=f"g16 < {label}.com > {label}.log",
    label=label,
    xc="PBE0",
    basis="Def2SVP",
    empiricaldispersion="GD3B",
    chk=label,
    charge=0,
    mult=3,
    scf=["qc", "maxcycle=100", "IntRep"],
    save=None,
    mem="40GB",
)

atoms.calc = calc
opt = GaussianOptimizer(atoms, calc=calc)
opt.run(fmax="tight", steps=250, opt="CalcFC")

e = atoms.get_potential_energy()
f = norm(max(atoms.get_forces(), key=norm))
print(f"final energy {e}")
print(f"max force {f}")

atoms.write("final.traj")

with pathlib.Path("final.e").open(mode="x", encoding="utf-8") as file:
    file.write(f"{e}\n")
