"""
Calculate fluoresence parameters
"""


def fvfm(fm, f0):
    """Calculate Fv/Fm

    Fv/Fm = (fm - f0) / fm

    :param fm: Fm
    :param f0: F0
    :returns: Fv/Fm (float)
    """

    return (fm - f0) / fm


def npq(fm, fmp):
    """Calculate NPQ

    NPQ = (fm - fmp) / fmp

    :param fm: Fm
    :param fmp: Fm'
    :returns: NPQ (float)
    """

    return (fm - fmp) / fmp


def npqt(fmp, f0p, fmf0=4.88):
    """Calculate NPQt

    NPQt = (4.88 / ((fmp / f0p) - 1)) - 1

    :param fmp: Fm'
    :param f0p: F0'
    :param fmf0: Fv/Fm (default: 4.88)
    :returns: NPQ (float)
    """

    return (fmf0 / ((fmp / f0p) - 1)) - 1


def phi2(fmp, fs):
    """Calculate Phi2

    Phi2 = (fmp - fs) / fmp

    :param fmp: Fm
    :param fs: Fs
    :returns: Phi2 (float)
    """

    return (fmp - fs) / fmp


def phino(fmp, fs, f0p, fm, f0):
    """Calculate PhiNO

    PhiNO = 1 / (npq + (1 + (ql * ((fm/f0)-1)))

    :param fmp: Fm'
    :param fs: Fs
    :param fmp: F0'
    :param fm: Fm
    :param f0: F0
    :returns: PhiNO (float)
    """

    ql_val = ql(fmp, fs, f0p)
    npq_val = npq(fm, fmp)
    return 1 / (npq_val + 1 + (ql_val * ((fm/f0)-1)))


def phinot(fmp, fs, f0p, fmf0=4.88):
    """Calculate PhiNOt

    PhiNOt = 1 / (npqt + (1 + (ql * 4.88)))

    :param fmp: Fm'
    :param fs: Fs
    :param fmf0: Fv/Fm (default: 4.88)
    :returns: PhiNOt (float)
    """

    ql_val = ql(fmp, fs, f0p)
    npqt_val = npqt(fmp, f0p, fmf0)
    return 1 / (npqt_val + (1 + (ql_val * fmf0)))


def phinpq(fmp, fs, f0p, fm, f0):
    """Calculate PhiNPQ

    PhiNPQ = 1 - (phi2 + phino)

    :param fmp: Fm'
    :param fs: Fs
    :param f0p: F0'
    :param fm: Fm
    :param f0: F0
    :returns: PhiNPQ (float)
    """

    phi2_val = phi2(fmp, fs)
    phino_val = phino(fmp, fs, f0p, fm, f0)
    return 1 - (phi2_val + phino_val)


def phinpqt(fmp, fs, f0p, fmf0=4.88):
    """Calculate PhiNPQt

    PhiNPQt = 1 - (phi2 + phinot)

    :param fmp: Fm'
    :param fs: Fs
    :param f0p: F0'
    :param fmf0: Fv/Fm (default: 4.88)
    :returns: PhiNOt (float)
    """

    phi2_val = phi2(fmp, fs)
    phinot_val = phinot(fmp, fs, f0p, fmf0)
    return 1 - (phi2_val + phinot_val)


def qe(fmpp, fmp):
    """Calculate qE

    qE = (fmpp - fmp) / fmp

    :param fmpp: Fm''
    :param fmp: Fm'
    :returns: qE (float)
    """

    return (fmpp - fmp) / fmp


def qesv(fm, fmp, fmpp):
    """Calculate qEsv

    qEsv = (fm / fmp) - (fm / fmpp)

    :param fm: Fm
    :param fmp: Fm'
    :param fmpp: Fm''
    :returns: qEsv (float)
    """

    return (fm / fmp) - (fm / fmpp)


def qet(fmp, f0p, fmpp, f0pp, fmf0=4.88):
    """Calculate qEt

    qEt = npqt - qit

    :param fmp: Fm'
    :param f0p: F0'
    :param fmpp: Fm''
    :param f0pp: F0''
    :param fmf0: Fv/Fm (default: 4.88)
    :returns: qEt (float)
    """

    npqt_val = npqt(fmp, f0p, fmf0)
    qit_val = qit(fmpp, f0pp, fmf0)
    return npqt_val - qit_val


def qi(fm, fmpp):
    """Calculate qI

    qI = (fm - fmpp) / fmpp

    :param fm: Fm
    :param fmpp: Fm''
    :returns: qI (float)
    """

    return (fm - fmpp) / fmpp


def qit(fmpp, f0pp, fmf0=4.88):
    """Calculate qIt

    qIt = (fmf0 / ((fmpp / f0pp) - 1)) - 1

    :param fmpp: Fm''
    :param f0pp: F0''
    :param fmf0: Fv/Fm (default: 4.88)
    :returns: qIt (float)
    """

    return (fmf0 / ((fmpp / f0pp) - 1)) - 1


def ql(fmp, fs, f0p):
    """Calculate qL

    qL = ((fmp - fs) / (fmp - f0p)) * (f0p / fs)

    :param fmp: Fm'
    :param fs: Fs
    :param f0p: F0'
    :returns: qL (float)
    """

    return ((fmp - fs) / (fmp - f0p)) * (f0p / fs)


def qp(fmp, fs, f0p):
    """Calculate qP

    qP = (fmp-fs)/(fmp-f0p)

    :param fmp: Fm'
    :param fs: Fs
    :param f0p: F0'
    :returns: qP (float)
    """

    return (fmp-fs)/(fmp-f0p)
