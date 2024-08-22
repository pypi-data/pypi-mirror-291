"""VASP calculation defaults."""

from collections.abc import MutableMapping

from autojob.calculation import calculators
from autojob.calculation import parameters


def _create_calculator_parameters() -> (
    MutableMapping[str, parameters.CalculatorParameter]
):
    algo = parameters.CalculatorParameter(
        name="ALGO",
        allowed_types=[str],
        special_values=(
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

    amix = parameters.NumberParameter(
        name="AMIX",
        allow_floats=True,
        description="linear mixing parameter for the magnetization density",
        number_range=parameters.NumberRange(
            lower_bound=0, lower_bound_exclusive=True
        ),
    )

    amix_mag = parameters.NumberParameter(
        name="AMIX_MAG",
        allow_floats=True,
        description="linear mixing parameter for the magnetization density",
        number_range=parameters.NumberRange(
            lower_bound=0, lower_bound_exclusive=True
        ),
    )

    bmix = parameters.NumberParameter(
        name="BMIX",
        allow_floats=True,
        description="sets the cutoff wave vector for Kerker mixing scheme",
        number_range=parameters.NumberRange(
            lower_bound=0, lower_bound_exclusive=True
        ),
    )

    bmix_mag = parameters.NumberParameter(
        name="BMIX_MAG",
        allow_floats=True,
        description="sets the cutoff wave vector for Kerker mixing scheme",
        number_range=parameters.NumberRange(
            lower_bound=0, lower_bound_exclusive=True
        ),
    )

    dipol = parameters.NumberSequenceParameter(
        name="DIPOL",
        allow_floats=True,
        special_values=(
            ("x-centre-of-mass", "y-centre-of-mass", "z-centre-of-mass"),
        ),
        description="the center of the "
        "cell in direct lattice coordinates with respect to which the total "
        "dipole-moment in the cell is calculated",
    )

    ediff = parameters.NumberParameter(
        name="EDIFF",
        allow_floats=True,
        default=1e-10,
        description="global break condition for the electronic SC-loop",
        number_range=parameters.NumberRange(
            lower_bound=0, lower_bound_exclusive=True
        ),
    )

    ediffg = parameters.NumberParameter(
        name="EDIFFG",
        allow_floats=True,
        description="break condition for the ionic relaxation loop",
    )

    encut = parameters.NumberParameter(
        name="ENCUT",
        allow_floats=True,
        default=450,
        description="cutoff energy for the plane-wave-basis set in eV",
        number_range=parameters.NumberRange(
            lower_bound=0, lower_bound_exclusive=True
        ),
    )

    gamma = parameters.CalculatorParameter(
        name="GAMMA",
        special_values=(True, False),
        default=False,
        description="whether the k-points include the \u0393 point",
    )

    gga = parameters.CalculatorParameter(
        name="GGA",
        special_values=(
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

    ibrion = parameters.CalculatorParameter(
        name="IBRION",
        special_values=(-1, 0, 1, 2, 3, 5, 6, 7, 8, 44),
        default=-1,
        description="how the ions are updated and moved",
    )

    icharg = parameters.CalculatorParameter(
        name="ICHARG",
        special_values=(0, 1, 2, 4, 10, 11, 12),
        description="construction of the initial charge density",
    )

    idipol = parameters.CalculatorParameter(
        name="IDIPOL",
        special_values=(0, 1, 2, 3, 4),
        description="monopole/dipole and quadrupole corrections to the total "
        "energy",
    )

    imix = parameters.CalculatorParameter(
        name="IMIX",
        special_values=(0, 1, 2, 4),
        description="the type of density mixing",
    )

    isif = parameters.NumberParameter(
        name="ISIF",
        special_values=(0, 1, 2, 3, 4, 5, 6, 7),
        default=2,
        description="whether the stress tensor is calculated and which "
        "principal "
        "degrees-of-freedom are allowed to change in relaxation and molecular "
        "dynamics runs",
    )

    ismear = parameters.NumberParameter(
        name="ISMEAR",
        default=0,
        description="how the partial occupancies are set for each orbital",
        number_range=parameters.NumberRange(
            lower_bound=-5, lower_bound_exclusive=False
        ),
    )

    ispin = parameters.CalculatorParameter(
        name="ISPIN",
        special_values=(1, 2),
        default=1,
        description="spin polarization",
    )

    istart = parameters.CalculatorParameter(
        name="ISTART",
        special_values=(0, 1, 2, 3),
        description="whether or not to read WAVECAR file",
    )

    isym = parameters.CalculatorParameter(
        name="ISYM",
        special_values=(-1, 0, 1, 2, 3),
        description="determines the way VASP treats symmetry",
    )

    ivdw = parameters.CalculatorParameter(
        name="IVDW",
        special_values=(0, 1, 10, 11, 12, 2, 20, 21, 202, 4),
        default=11,
        description="vdW dispersion correction",
    )

    kpts = parameters.NumberSequenceParameter(
        name="KPTS",
        default=(4, 4, 1),
        description="k-point grid for Brillouin-zone sampling",
        number_range=parameters.NumberRange(
            lower_bound=1, lower_bound_exclusive=False
        ),
    )

    kpar = parameters.NumberParameter(
        name="KPAR",
        default=4,
        description="number of k-points to be treated in parallel",
        number_range=parameters.NumberRange(
            lower_bound=1, lower_bound_exclusive=False
        ),
    )

    ldau = parameters.CalculatorParameter(
        name="LDAU",
        special_values=(True, False),
        description="DFT+U",
    )

    ldau_type = parameters.CalculatorParameter(
        name="LDAUTYPE",
        special_values=(1, 2, 3, 4),
        description="the DFT+U variant that will be used",
    )

    ldauj = parameters.NumberSequenceParameter(
        name="LDAUJ",
        allow_floats=True,
        description="strength of the effective on-site exchange interactions",
        number_range=parameters.NumberRange(
            lower_bound=0, lower_bound_exclusive=False
        ),
    )

    ldaul = parameters.NumberSequenceParameter(
        name="LDAUL",
        description="the l-quantum number for which the on-site interaction "
        "is added",
        number_range=parameters.NumberRange(
            lower_bound=-1,
            lower_bound_exclusive=False,
            upper_bound=6,
            upper_bound_exclusive=False,
        ),
    )

    ldauu = parameters.NumberSequenceParameter(
        name="LDAUU",
        description="strength of the effective on-site Coulomb interactions",
        number_range=parameters.NumberRange(
            lower_bound=0, lower_bound_exclusive=False
        ),
    )

    ldipol = parameters.CalculatorParameter(
        name="LDIPOL",
        special_values=(True, False),
        default=False,
        description="switches on corrections to the potential and forces",
    )

    lmaxmix = parameters.CalculatorParameter(
        name="LMAXMIX",
        special_values=(0, 1, 2, 3, 4, 5, 6),
        description=(
            "up to which l-quantum number the one-center PAW charge "
            "densities are passed through the charge density mixer and "
            "written to the CHGCAR file"
        ),
    )

    lorbit = parameters.CalculatorParameter(
        name="LORBIT",
        special_values=(0, 1, 2, 5, 10, 11, 12, 13, 14),
        description=(
            "determines whether the PROCAR or PROOUT files are written"
        ),
    )

    lplane = parameters.CalculatorParameter(
        name="LPLANE",
        special_values=(True, False),
        default=True,
        description="plane-wise data distribution in real space",
    )

    lreal = parameters.CalculatorParameter(
        name="LREAL",
        special_values=(True, False, "On", "Auto"),
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

    magmom = parameters.NumberSequenceParameter(
        name="MAGMOM",
        description="initial magnetic moment for each atom",
        number_range=parameters.NumberRange(),
    )

    nbands = parameters.NumberParameter(
        name="NBANDS",
        description="total number of KS or QP orbitals in the calculation",
        number_range=parameters.NumberRange(
            lower_bound=1, lower_bound_exclusive=False
        ),
    )

    ncore = parameters.NumberParameter(
        name="NCORE",
        default=2,
        description="number of compute cores that work on an individual "
        "orbital",
        number_range=parameters.NumberRange(
            lower_bound=1, lower_bound_exclusive=False
        ),
    )

    nelm = parameters.NumberParameter(
        name="NELM",
        default=60,
        description="maximum number of electronic SC (self-consistency) steps",
        number_range=parameters.NumberRange(
            lower_bound=1, lower_bound_exclusive=False
        ),
    )

    npar = parameters.NumberParameter(
        name="NPAR",
        description="number of bands that are treated in parallel",
        number_range=parameters.NumberRange(
            lower_bound=1, lower_bound_exclusive=False
        ),
    )

    nsw = parameters.NumberParameter(
        name="NSW",
        default=0,
        description="maximum number of ionic steps",
        number_range=parameters.NumberRange(
            lower_bound=0, lower_bound_exclusive=False
        ),
    )

    potim = parameters.NumberParameter(
        name="POTIM",
        allow_floats=True,
        description="gives the time step (in fs) in all ab-initio Molecular "
        "Dynamics runs; scaling constant for step widths",
        number_range=parameters.NumberRange(lower_bound=0),
    )

    prec = parameters.CalculatorParameter(
        name="PREC",
        special_values=(
            "Low",
            "Medium",
            "High",
            "Normal",
            "Single",
            "Accurate",
        ),
        default="Accurate",
        description="precision-mode",
    )

    sigma = parameters.NumberParameter(
        name="SIGMA",
        allow_floats=True,
        default=0.04,
        description="width of the smearing in eV",
        number_range=parameters.NumberRange(lower_bound=0),
    )

    smass = parameters.NumberParameter(
        name="SMASS",
        allow_floats=True,
        special_values=(-3, -2, -1),
        description="controls the velocities "
        "during an ab-initio molecular-dynamics run",
        number_range=parameters.NumberRange(lower_bound=0),
    )

    params = (
        algo,
        amix,
        amix_mag,
        bmix,
        bmix_mag,
        dipol,
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
        kpts,
        kpar,
        ldau_type,
        ldau,
        ldauj,
        ldaul,
        ldauu,
        ldipol,
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
    )

    return {p.name: p for p in params}


CALCULATOR_PARAMETERS = _create_calculator_parameters()
DEFAULT_CONFIGURATION = calculators.CalculatorConfiguration(
    CALCULATOR_PARAMETERS.values()
)
