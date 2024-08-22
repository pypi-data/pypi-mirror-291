"""Define Gaussian calculation parameters."""

import math
from typing import ClassVar
from typing import TypeVar

from autojob.coordinator import job

S = TypeVar("S", bound="GaussianJob")


# TODO: Implement compound Gaussian jobs
# e.g.: method2/basis2 // method1/basis1
class GaussianJob(job.Job):
    """A class to represent a Gaussian job."""

    FILES: ClassVar[list[tuple[str, bool]]] = [
        ("Gaussian.log", False),  # filename, required?
        ("Gaussian.chk", False),
    ]

    @staticmethod
    def _create_input_params() -> list[job.CalculationParameter]:
        command = job.CalculationParameter(
            name="command",
            explicit=False,
            default="g16 < Gaussian.com > Gaussian.log",
            allowed_types=[str],
            values=(None, None, None),
            description="specifies the form of the command used to call "
            "Gaussian",
        )
        addsec = job.CalculationParameter(
            name="addsec",
            explicit=False,
            allowed_types=[str],
            values=(None, None, None),
            description="Text to be added after the molecular geometry "
            "specification, e.g. for defining constraints with "
            "opt='modredundant'",
        )
        mem = job.CalculationParameter(
            name="mem",
            explicit=False,
            allowed_types=[str],
            default="10GB",
            values=(None, None, None),
            description="specifies the amount of memory requested",
        )
        save = job.CalculationParameter(
            name="save",
            explicit=False,
            allowed_types=[str],
            default=None,
            values=(None, None, None),
            description="specifies which scratch files to save",
        )
        label = job.CalculationParameter(
            name="label",
            explicit=False,
            allowed_types=[str],
            values=(None, None, None),
            default="Gaussian",
            description="specifies how to name checkpoint files",
        )
        xc = job.CalculationParameter(
            name="xc",
            explicit=True,
            allowed_types=[str],
            values=(
                "pbe",
                "pbe0",
                "hse06",
                "hse03",
                "lda",
                "tpss",
                "revtpss",
            ),
            default="pbe0",
            description="LDA or GGA exchange-correlation functional",
        )

        basis = job.CalculationParameter(
            name="basis",
            explicit=False,
            allowed_types=[str],
            values=(None, None, None),
            specials=[
                "STO-3G",
                "6-31G",
                "6-31G*",
                "6-31G**",
                "Def2SVP",
                "Def2TZVP",
                "Def2TZVPP",
            ],
            default="Def2SVP",
            description="basis set to use",
        )

        basisfile = job.CalculationParameter(
            name="basisfile",
            explicit=False,
            allowed_types=[str],
            values=(None, None, None),
            description="specifies a basis file to be used",
        )

        basis_set = job.CalculationParameter(
            name="basis_set",
            explicit=False,
            allowed_types=[str],
            values=(None, None, None),
            description=(
                "specifies a string version of a basis file to be used"
                ". You should probably also set 'basis'='gen' too."
            ),
        )

        empiricaldispersion = job.CalculationParameter(
            name="empiricaldispersion",
            explicit=True,
            allowed_types=[str],
            values=("PFD", "GD2", "wB97XD", "GD3", "GD3BJ"),
            default="GD3BJ",
            description="enables empirical dispersion",
        )

        method = job.CalculationParameter(
            name="method",
            explicit=False,
            allowed_types=[str],
            values=(None, None, None),
            specials=[
                "B3LYP",
                "wB97XD",
                "PBE1PBE",
                "HSEH1PBE",
                "OHSE2PBE",
                "PBE",
                "TPSS",
                "RevTPSS",
            ],
            description="The level of theory to use",
        )

        charge = job.CalculationParameter(
            name="charge",
            explicit=False,
            allowed_types=[int],
            values=(-math.inf, math.inf, "()"),
            default=0,
            description="the system charge",
        )

        mult = job.CalculationParameter(
            name="mult",
            explicit=False,
            allowed_types=[int],
            values=(-math.inf, math.inf, "()"),
            default=1,
            description="the system multiplicity (spin + 1)",
        )

        scf = job.CalculationParameter(
            name="scf",
            explicit=False,
            allowed_types=[str],
            values=(None, None, None),
            default="qc,maxcycle=100,IntRep",
            description="SCF convergence settings",
        )

        opt = job.CalculationParameter(
            name="opt",
            explicit=False,
            allowed_types=[str],
            values=(None, None, None),
            default="Tight,MaxCycles=250,CalcFC",
            description="optimization parameters",
        )

        return [
            command,
            addsec,
            mem,
            save,
            label,
            xc,
            basis,
            basisfile,
            basis_set,
            empiricaldispersion,
            method,
            charge,
            mult,
            scf,
            opt,
        ]

    # ? Convert to abstract static property
    @staticmethod
    def input_parameters() -> list[job.CalculationParameter]:
        """Generate Gaussian job input parameters."""
        return GaussianJob._input_parameters.copy()

    _input_parameters = _create_input_params()
