import json

from ase import Atoms
from ase.build import bulk
from ase.build import molecule
import pytest

from autojob import MyEncoder
from autojob import my_object_hook


@pytest.fixture(
    name="atoms",
    params=[
        Atoms("C"),
        bulk("Cu"),
        molecule("NH3"),
    ],
)
def fixture_atoms(request: pytest.FixtureRequest) -> Atoms:
    atoms: Atoms = request.param
    return atoms


def test_should_recreate_atoms_from_json(atoms: Atoms) -> None:
    dumped_atoms = json.dumps(atoms, indent=4, cls=MyEncoder)
    atoms_clone = json.loads(dumped_atoms, object_hook=my_object_hook)

    assert atoms == atoms_clone
