"""Parametrize VASP calculations.

.. deprecated:: Use :mod:`autojob.calculation.vasp` instead.
"""

import math
from typing import ClassVar
from typing import TypeVar

from autojob.coordinator import job

S = TypeVar("S", bound="VaspJob")


class VaspError(Exception):
    """A VASP error."""


class VaspJob(job.Job):
    """A VASP job."""

    FILES: ClassVar[tuple[str, bool]] = [
        ("CHGCAR", False),  # filename, required?
        ("WAVECAR", False),
    ]

    @staticmethod
    def _create_input_params() -> list[job.CalculationParameter]:
        algo = job.CalculationParameter(
            "ALGO",
            True,
            [str],
            (
                "Normal",
                "VeryFast",
                "Old VeryFast",
                "Fast",
                "Old Fast",
                "Damped",
                "Exact",
                "Subrot",
                "Eigenval",
                "None",
                "Nothing",
            ),
            default="Fast",
            description="electronic minimization, algorithm",
        )

        amix = job.CalculationParameter(
            "AMIX",
            False,
            [float],
            (0, math.inf, "()"),
            description="linear mixing parameter for the magnetization "
            "density",
        )

        amix_mag = job.CalculationParameter(
            "AMIX_MAG",
            False,
            [float],
            (0, math.inf, "()"),
            description="linear mixing parameter for the magnetization "
            "density",
        )

        bmix = job.CalculationParameter(
            "BMIX",
            False,
            [float],
            (0, math.inf, "()"),
            description="sets the cutoff wave vector for Kerker mixing scheme",
        )

        bmix_mag = job.CalculationParameter(
            "BMIX_MAG",
            False,
            [float],
            (0, math.inf, "()"),
            description="sets the cutoff wave vector for Kerker mixing scheme",
        )

        dipolx = job.CalculationParameter(
            "DIPOL_X",
            False,
            [float],
            (-math.inf, math.inf, "()"),
            default=None,
            description="the center of the "
            "cell in direct lattice coordinates "
            "with respect to which the total "
            "dipole-moment in the cell is "
            "calculated",
            specials=["x-centre-of-mass", None],
        )

        dipoly = job.CalculationParameter(
            "DIPOL_Y",
            False,
            [float],
            (-math.inf, math.inf, "()"),
            default=None,
            description="the center of the "
            "cell in direct lattice coordinates "
            "with respect to which the total "
            "dipole-moment in the cell is "
            "calculated",
            specials=["y-centre-of-mass", None],
        )

        dipolz = job.CalculationParameter(
            "DIPOL_Z",
            False,
            [float],
            (-math.inf, math.inf, "()"),
            default=None,
            description="the center of the "
            "cell in direct lattice coordinates "
            "with respect to which the total "
            "dipole-moment in the cell is "
            "calculated",
            specials=["z-centre-of-mass", None],
        )

        ediff = job.CalculationParameter(
            "EDIFF",
            False,
            [float],
            (0, math.inf, "()"),
            default=1e-10,
            description="global break condition for the electronic SC-loop",
        )

        ediffg = job.CalculationParameter(
            "EDIFFG",
            False,
            [float],
            (-math.inf, math.inf, "()"),
            default=-1e-2,
            description="break condition for the ionic relaxation loop",
        )

        encut = job.CalculationParameter(
            "ENCUT",
            False,
            [float],
            (0, math.inf, "()"),
            default=450,
            description="cutoff energy for the plane-wave-basis set in eV",
            specials=[None],
        )

        gamma = job.CalculationParameter(
            "GAMMA",
            True,
            [bool],
            (True, False),
            default=False,
            description="whether the k-points include the \u0393 point",
        )

        gga = job.CalculationParameter(
            "GGA",
            True,
            [str],
            (
                "CA",
                "PZ",
                "VW",
                "HL",
                "WI",
                "LIBXC",
                "LI",
                "91",
                "PE",
                "RE",
                "RP",
                "PS",
                "AM",
                "B3",
                "B5",
                "BF",
                "OR",
                "BO",
                "MK",
                "ML",
                "CX",
            ),
            default="PE",
            description="LDA or GGA exchange-correlation functional",
        )

        ibrion = job.CalculationParameter(
            "IBRION",
            True,
            [int],
            (-1, 0, 1, 2, 3, 5, 6, 7, 8, 44),
            default=2,
            description="how the ions are updated and moved",
        )

        icharg = job.CalculationParameter(
            "ICHARG",
            True,
            [int],
            (0, 1, 2, 4, 10, 11, 12),
            description="construction of the initial charge density",
        )

        idipol = job.CalculationParameter(
            "IDIPOL",
            False,
            [int],
            (1, 4, "[]"),
            description="monopole/dipole and "
            "quadrupole corrections to the "
            "total energy",
            specials=[None],
        )

        imix = job.CalculationParameter(
            "IMIX",
            True,
            [float],
            (0, 1, 2, 4),
            description="the type of density mixing",
        )

        isif = job.CalculationParameter(
            "ISIF",
            False,
            [int],
            (0, 7, "[]"),
            default=2,
            description="whether the stress tensor "
            "is calculated and which principal "
            "degrees-of-freedom are allowed to "
            "change in relaxation and molecular "
            "dynamics runs",
        )

        ismear = job.CalculationParameter(
            "ISMEAR",
            False,
            [int],
            (-5, math.inf, "[)"),
            default=0,
            description="how the partial "
            "occupancies are set for each "
            "orbital",
        )

        ispin = job.CalculationParameter(
            "ISPIN",
            True,
            [int],
            (1, 2),
            default=2,
            description="spin polarization",
        )

        istart = job.CalculationParameter(
            "ISTART",
            False,
            [int],
            (0, 3, "[]"),
            description="whether or not to read WAVECAR file",
        )

        isym = job.CalculationParameter(
            "ISYM",
            False,
            [int],
            (-1, 3, "[]"),
            description="determines the way VASP treats symmetry",
        )

        ivdw = job.CalculationParameter(
            "IVDW",
            True,
            [int],
            (0, 1, 10, 11, 12, 2, 20, 21, 202, 4),
            default=11,
            description="vdW dispersion correction",
        )

        kptx = job.CalculationParameter(
            "KPTS_X",
            False,
            [int],
            (0, math.inf, "()"),
            default=4,
            description="number of k-points in the "
            "x-direction for Brillouin-zone sampling",
        )

        kpty = job.CalculationParameter(
            "KPTS_Y",
            False,
            [int],
            (0, math.inf, "()"),
            default=4,
            description="number of k-points in the "
            "y-direction for Brillouin-zone sampling",
        )

        kptz = job.CalculationParameter(
            "KPTS_Z",
            False,
            [int],
            (0, math.inf, "()"),
            default=1,
            description="number of k-points in the "
            "z-direction for Brillouin-zone sampling",
        )

        kpar = job.CalculationParameter(
            "KPAR",
            False,
            [int],
            (0, math.inf, "()"),
            default=4,
            description="number of k-points to be treated in parallel",
        )

        ldau = job.CalculationParameter(
            "LDAU",
            True,
            [bool],
            (True, False),
            description="DFT+U",
        )

        ldau_type = job.CalculationParameter(
            "LDAUTYPE",
            False,
            [int],
            (1, 4, "[]"),
            description="the DFT+U variant that will be used",
        )

        ldauj = job.CalculationParameter(
            "LDAUJ",
            False,
            [int],  # change to Tuple
            (-math.inf, math.inf, "()"),
            description="strength of the effective on-site exchange "
            "interactions",
        )

        ldaul = job.CalculationParameter(
            "LDAUL",
            False,
            [float],
            (-math.inf, math.inf, "()"),
            description="the l-quantum number for which the on-site "
            "interaction is added",
        )

        ldauu = job.CalculationParameter(
            "LDAUU",
            False,
            [int],
            (-math.inf, math.inf, "()"),
            description="strength of the effective on-site Coulomb "
            "interactions",
        )

        ldipol = job.CalculationParameter(
            "LDIPOL",
            True,
            [bool],
            (True, False),
            default=False,
            description="switches on corrections to "
            "the potential and forces",
        )

        lepsilon = job.CalculationParameter(
            "LEPSILON",
            True,
            [bool],
            (True, False),
            description="enables to calculate and to print the BEC tensors",
        )

        lmaxmix = job.CalculationParameter(
            "LMAXMIX",
            False,
            [int],
            (0, math.inf, "()"),
            default=4,
            description=(
                "up to which l-quantum number the one-center PAW charge "
                "densities are passed through the charge density mixer and "
                "written to the CHGCAR file"
            ),
        )

        lorbit = job.CalculationParameter(
            "LORBIT",
            True,
            [int],
            (0, 1, 2, 5, 10, 11, 12, 13, 14),
            default=11,
            description=(
                "determines whether the PROCAR or PROOUT files are written"
            ),
        )

        lplane = job.CalculationParameter(
            "LPLANE",
            True,
            [bool],
            (True, False),
            default=True,
            description="plane-wise data distribution in real space",
        )

        lreal = job.CalculationParameter(
            "LREAL",
            True,
            [bool],
            (True, False, "On", "Auto"),
            default="Auto",
            description="determines whether the projection operators are "
            "evaluated in real-space or in reciprocal space",
        )

        # lsmp2lt = job.InputParameter("LSMP2LT",
        #                              True,
        #                              [bool, NoneType],
        #                              (True, False, None),
        #                              default=None,
        #                              description="select the Laplace "
        #                              + "transformed MP2 algorithm")

        magmom = job.CalculationParameter(
            "MAGMOM",
            False,
            [str],
            (),
            description="initial magnetic moment for each atom",
        )

        nbands = job.CalculationParameter(
            "NBANDS",
            False,
            [int],
            (1, math.inf, "[)"),
            description="total number of KS "
            "or QP orbitals in the calculation",
        )

        ncore = job.CalculationParameter(
            "NCORE",
            False,
            [int],
            (1, math.inf, "[)"),
            default=4,
            description="number of compute cores "
            "that work on an individual orbital",
        )

        nelm = job.CalculationParameter(
            "NELM",
            False,
            [int],
            (1, math.inf, "[)"),
            default=250,
            description="maximum number of electronic "
            "SC (self-consistency) steps",
        )

        npar = job.CalculationParameter(
            "NPAR",
            False,
            [int],
            (1, math.inf, "[)"),
            description="number of bands that are treated in parallel",
        )

        nsw = job.CalculationParameter(
            "NSW",
            False,
            [int],
            (0, math.inf, "[)"),
            default=1000,
            description="maximum number of ionic steps",
        )

        potim = job.CalculationParameter(
            "POTIM",
            False,
            [float],
            (0, math.inf, "()"),
            default=0.5,
            description="gives the time step (in fs) "
            "in all ab-initio Molecular Dynamics "
            "runs; scaling constant for step widths",
        )

        prec = job.CalculationParameter(
            "PREC",
            True,
            [str],
            ("Low", "Medium", "High", "Normal", "Single", "Accurate"),
            default="Accurate",
            description="precision-mode",
        )

        sigma = job.CalculationParameter(
            "SIGMA",
            False,
            [float],
            (0, math.inf, "()"),
            default=0.04,
            description="width of the smearing in eV",
        )

        smass = job.CalculationParameter(
            "SMASS",
            False,
            [float],
            (0, math.inf, "[)"),
            default=-3,
            description="controls the velocities "
            "during an ab-initio molecular-dynamics "
            "run",
            specials=[-3, -2, -1],
        )

        return [
            algo,
            amix,
            amix_mag,
            bmix,
            bmix_mag,
            dipolx,
            dipoly,
            dipolz,
            ediff,
            ediffg,
            encut,
            gga,
            gamma,
            ibrion,
            icharg,
            idipol,
            imix,
            isif,
            ismear,
            ispin,
            istart,
            isym,
            ivdw,
            kptx,
            kpty,
            kptz,
            kpar,
            ldau_type,
            ldau,
            ldauj,
            ldaul,
            ldauu,
            ldipol,
            lepsilon,
            lmaxmix,
            lorbit,
            lplane,
            lreal,
            magmom,
            nbands,
            ncore,
            nelm,
            npar,
            nsw,
            potim,
            prec,
            sigma,
            smass,
        ]

    # ? Convert to abstract static property
    @staticmethod
    def input_parameters() -> list[job.CalculationParameter]:
        """A list of VASP calculation parameters."""
        return VaspJob._input_parameters.copy()

    _input_parameters = _create_input_params()
