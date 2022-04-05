"""
Calculate additional fluoresence parameters

These parameters are based on the standard parameters calculated
"""


def lef(phi2, par, absorptivity=0.5):
    """Calculate LEF

    LEF = phi * absorptivity * par

    :param phi2: PhiNOt
    :param par: Light Intensity in µE×s⁻¹×m⁻² (PAR)
    :param absorptivity: Leaf absorbtivity (default 0.5)
    :returns: Vx (float)
    """
    return phi2 * absorptivity * par


def vx(phinot, ql, absorptivity=0.5):
    """Calculate Vx

    Vx = phinot * absorptivity * (1-ql)

    :param phinot: PhiNOt
    :param ql: qL
    :param absorptivity: Leaf absorbtivity (default 0.5)
    :returns: Vx (float)
    """
    return phinot * absorptivity * (1-ql)


def sphi2(phi2, phinot, ql, phinoopt=0.2, fmf0=4.88):
    """Calculate S~Phi2

    S~Phi2 = phi2 * 1 / (1 + phi2 * (1/phinoopt - 1/phinot) / (ql * fmf0) )

    :param phi2: Phi2
    :param phinot: PhiNOt
    :param ql: qL
    :param phinoopt: Optimum PhiNO (default: 0.2)
    :param fmf0: Fv/Fm (default: 4.88)
    :returns: SPhi2 (float)
    """
    return phi2 * 1 / (1 + phi2 * (1/phinoopt - 1/phinot) / (ql * fmf0))


def sphinpq(phi2, phinot, ql, phinoopt=0.2, fmf0=4.88):
    """Calculate S~PhiNPQ

    S~PhiNPQ = 1 - ((phi2 * 1 / (1 + phi2 * (1/phinoopt - 1/phinot) / (ql * fmf0) ))+fmf0)

    :param phi2: Phi2
    :param phinot: PhiNOt
    :param ql: qL
    :param phinoopt: Optimum PhiNO (default: 0.2)
    :param fmf0: Fv/Fm (default: 4.88)
    :returns: SPhiNPQ (float)
    """
    return 1 - ((phi2 * 1 / (1 + phi2 * (1/phinoopt - 1/phinot) / (ql * fmf0)))+phinoopt)


def deltanpq(phino, phinoopt=0.2):
    """Calculate deltaNPQ

    deltaNPQ = (1/phinoopt) - (1/phino)

    :param phino: PhiNO
    :param phinoopt: Optimum PhiNO (default: 0.2)
    :returns: deltaNPQ (float)
    """
    return (1/phinoopt) - (1/phino)
