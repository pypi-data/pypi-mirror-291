import pytest

pytest.skip(allow_module_level=True)
import pathlib

from ase.calculators.vasp import Vasp
import ase.io
from numpy.linalg import norm

ldau_luj = {
    "H": {"L": -1, "U": 0, "J": 0},
    "N": {"L": -1, "U": 0, "J": 0},
    "O": {"L": -1, "U": 0, "J": 0},
    "S": {"L": -1, "U": 0, "J": 0},
    "Ag": {"L": 2, "U": 3.87, "J": 0},
    "Co": {"L": 2, "U": 5.2, "J": 0},
    "Mn": {"L": 2, "U": 5.3, "J": 0},
    "Ni": {"L": 2, "U": 6.1, "J": 0},
}

atoms = ase.io.read("Ag-Co-Ni-BHT.traj")

calc = Vasp(
    algo="Normal",
    ediff=1e-08,
    ediffg=-0.01,
    encut=550,
    gga="PE",
    gamma=False,
    ibrion=2,
    isif=2,
    ismear=0,
    ispin=2,
    ivdw=11,
    kpar=4,
    ldautype=3,
    ldau=True,
    ldipol=False,
    lmaxmix=4,
    lorbit=11,
    lplane=True,
    lreal="Auto",
    ncore=4,
    nelm=250,
    nsw=1000,
    potim=0.4,
    prec="Accurate",
    sigma=0.04,
    smass=-3,
    kpts=(4, 4, 1),
    dipol=None,
    ldau_luj={
        "H": {"L": -1, "U": 0, "J": 0},
        "N": {"L": -1, "U": 0, "J": 0},
        "O": {"L": -1, "U": 0, "J": 0},
        "S": {"L": -1, "U": 0, "J": 0},
        "Ag": {"L": 2, "U": 3.87, "J": 0},
        "Co": {"L": 2, "U": 5.2, "J": 0},
        "Mn": {"L": 2, "U": 5.3, "J": 0},
        "Ni": {"L": 2, "U": 6.1, "J": 0},
    },
)

atoms.calc = calc
e = atoms.get_potential_energy()
f = norm(max(atoms.get_forces(), key=norm))

print(f"final energy {e} eV")
print(f"max force {f} eV/Å")

atoms.set_initial_magnetic_moments(atoms.get_magnetic_moments())
atoms.write("final.traj")

with pathlib.Path("final.e").open(mode="x", encoding="utf-8") as file:
    file.write(f"{e}\n")
