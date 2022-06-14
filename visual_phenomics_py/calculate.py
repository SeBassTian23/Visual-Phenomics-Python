"""
Calculate additional parameters or recalculate parameters.
"""

from visual_phenomics_py.util.parameters import fvfm, npq, npqt, phi2, phino, phinot, phinpq, phinpqt, qe, qesv, qet, qi, qit, ql, qp
from visual_phenomics_py.util.parameters_additional import lef, vx, sphi2, sphinpq


def calculate(df=None, param='', *, fm='fm', f0='f0', fmp='fmp', f0p='f0p', fs='fs', fmpp='fmpp', f0pp='f0pp', fmf0=4.88, alias=None):
    """Calculate photosynthetic parameters

    Calculate photosynthetic parameters from basic fluorescence parameters

    :param df: The DataFrame to add the calculated parameters to.
    :param param: Parameter to calculate ('Fvfm','NPQ', 'NPQt','Phi2','PhiNO','PhiNPQ','qE','qEsv','qEt','qI','qIt','qL','qP')
    :param fm: fm column name (default 'fm')
    :param f0: f0 column name (default 'f0')
    :param fmp: fmp column name (default 'fmp')
    :param f0p: f0p column name (default 'f0p')
    :param fs: fs column name (default 'fs')
    :param fmpp: fmpp column name (default 'fmpp')
    :param f0pp: f0pp column name (default 'f0pp')
    :param fmf0: Fm/F0 for t parameter (default 4.88)
    :param alias: rename the selected parameter (default None)
    :returns: a dataframe column for the calculated parameter
    """

    # Parameter Names
    parameters = ['Fvfm', 'NPQ', 'NPQt', 'Phi2', 'PhiNO', 'PhiNOt',
                  'PhiNPQ', 'PhiNPQt', 'qE', 'qEsv', 'qEt', 'qI', 'qIt', 'qL', 'qP']

    if df is None:
        raise Exception('No DataFrame selected.')
    if (param in parameters):
        alias_txt = ""
        if alias is not None:
            alias_txt = " as {0}".format(alias)

        print('Calculating {0}{1}'.format(param, alias_txt))

        ## Make sure only the fm and f0 values are filled, as they are the only columns
        ## need fillna for calculations.
        df_tmp = df.sort_values(by=['sample', 'time'], ascending=True)
        df_tmp[[fm,f0]] = df_tmp[[fm,f0]].fillna(method="ffill")

        for row in df_tmp.sort_values(by=['sample', 'time'], ascending=True).itertuples():
            if param == 'Fvfm':
                if {fm, f0}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = fvfm(
                        getattr(row, fm), getattr(row, f0))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fm and f0')

            elif param == 'NPQ':
                if {fm, fmp}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = npq(
                        getattr(row, fm), getattr(row, fmp))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fm and fmp')

            elif param == 'NPQt':
                if {fmp, f0p}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = npqt(
                        getattr(row, fmp), getattr(row, f0p), fmf0)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp and f0p')

            elif param == 'Phi2':
                if {fmp, fs}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = phi2(
                        getattr(row, fmp), getattr(row, fs))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp and fs')

            elif param == 'PhiNO':
                if {fmp, fs, f0p, fm, f0}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = phino(getattr(row, fmp), getattr(
                        row, fs), getattr(row, f0p), getattr(row, fm), getattr(row, f0))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp, fs, fm, and f0')

            elif param == 'PhiNOt':
                if {fmp, fs, f0p}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = phinot(
                        getattr(row, fmp),  getattr(row, fs), getattr(row, f0p), fmf0)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp, fs, and f0p')

            elif param == 'PhiNPQ':
                if {fmp, fs, f0p, fm, f0}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = phinpq(getattr(row, fmp), getattr(
                        row, fs), getattr(row, f0p), getattr(row, fm), getattr(row, f0))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp, fs, f0p, fm, and f0')

            elif param == 'PhiNPQt':
                if {fmp, fs, f0p}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = phinpqt(
                        getattr(row, fmp), getattr(row, fs), getattr(row, f0p), fmf0)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp, fs, and f0p')

            elif param == 'qE':
                if {fmpp, fmp}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = qe(
                        getattr(row, fmpp), getattr(row, fmp))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmpp and fmp')

            elif param == 'qEsv':
                if {fm, fmp, fmpp}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = qesv(
                        getattr(row, fm), getattr(row, fmp), getattr(row, fmpp))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fm, fmp, and fmpp')

            elif param == 'qEt':
                if {fmp, f0p, fmpp, f0pp}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = qet(getattr(row, fmp), getattr(
                        row, f0p), getattr(row, fmpp), getattr(row, f0pp), fmf0)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp, f0p, fmpp, and f0pp')

            elif param == 'qI':
                if {fm, fmpp}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = qi(
                        getattr(row, fm), getattr(row, fmpp))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fm and fmpp')

            elif param == 'qIt':
                if {fmpp, f0pp}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = qit(
                        getattr(row, fmpp), getattr(row, f0pp), fmf0)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmpp and f0pp')

            elif param == 'qL':
                if {fmp, fs, f0p}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = ql(
                        getattr(row, fmp), getattr(row, fs), getattr(row, f0p))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp, fs, and f0p')

            elif param == 'qP':
                if {fmp, fs, f0p}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = qp(
                        getattr(row, fmp), getattr(row, fs), getattr(row, f0p))
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp, fs, and f0p')

            else:
                raise Exception("No matching parameter found.")

        ## Write column to DataFrame
        df[alias or param] = df_tmp[alias or param]
    else:
        raise Exception('Unknown parameter. Available parameters are: {0}'.format(
            ", ".join(parameters)))


def calculate_additional(df=None, param='', *, v_phino='PhiNOt', v_phi2='Phi2', v_ql='qL', v_par='light_intensity', phinoopt=0.2, absorptivity=0.5, fmf0=4.88, alias=None):
    """Calculate additional Parameters

    Calculate additional photosynthetic parameters based on calculated standard parameters

    :param df: The DataFrame to add the calculated parameters to.
    :param param: Parameter to calculate ('LEF', 'Vx', 'SPhi2', 'SNPQ', 'deltaNPQ')
    :param v_phino: PhiNO column name (default 'PhiNOt')
    :param v_phi2: Phi2 column name (default 'Phi2')
    :param v_ql: qL column name (default 'qL')
    :param phinoopt: Optimal PhiNO (default 0.2)
    :param absorptivity: Absorptivity for Vx parameter (default 0.5)
    :param fmf0: Fm/F0 for t parameter (default 4.88)
    :param alias: rename the selected parameter (default None)
    :returns: a dataframe column for the calculated parameter
    """

    # Parameter Names
    parameters = ['LEF', 'Vx', 'SPhi2', 'SNPQ', 'deltaNPQ']

    if df is None:
        raise Exception('No DataFrame selected.')

    if (param in parameters):
        alias_txt = ""
        if alias is not None:
            alias_txt = " as {0}".format(alias)

        print('Calculating {0}{1}'.format(param, alias_txt))

        ## No Parameter needs filling at this time
        df_tmp = df.sort_values(by=['sample', 'time'], ascending=True)
        # df_tmp[[fm,f0]] = df_tmp[[fm,f0]].fillna(method="ffill")

        for row in df_tmp.sort_values(by=['sample', 'time'], ascending=True).itertuples():
            if param == 'LEF':
                if {v_phi2, v_par}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = lef(
                        getattr(row, v_phi2), getattr(row, v_par), absorptivity)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for v_phi2 and v_par')

            elif param == 'Vx':
                if {v_phino, v_phi2, v_par}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = vx(
                        getattr(row, v_phino), getattr(row, v_phi2), getattr(row, v_par), absorptivity)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for v_phino, v_phi2, and v_par')

            elif param == 'SPhi2':
                if {v_phino, v_phi2, v_ql}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = sphi2(
                        getattr(row, v_phi2), getattr(row, v_phino), getattr(row, v_ql), phinoopt, fmf0)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for v_phino, v_phi2, and v_ql')

            elif param == 'SNPQ':
                if {v_phino, v_phi2}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = sphinpq(
                        getattr(row, v_phi2), getattr(row, v_phino), getattr(row, v_ql), phinoopt, fmf0)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for v_phino, v_phi2, and v_ql')

            elif param == 'deltaNPQ':
                if {v_phino}.issubset(df_tmp.columns):
                    df_tmp.at[row.Index, alias or param] = deltanpq(
                        getattr(row, v_phino), phinoopt)
                else:
                    raise Exception(
                        'Missing parameter(s). Define columns for fmp, fs, and f0p')

            else:
                raise Exception("No matching parameter found.")

        ## Write column to DataFrame
        df[alias or param] = df_tmp[alias or param]
    else:
        raise Exception('Unknown parameter. Available parameters are: {0}'.format(
            ", ".join(parameters)))


def calculate_custom(df=None, name='', fn=None, *, cols=[], fill=[], params={}):
    """Calculate additional Parameters

    Use a custom function to calculate a custom parameter.

    :param df: The DataFrame to add the calculated parameters to.
    :param name: Parameter name
    :param fn: Function name for the calculation
    :param cols: Column names for parameters passed to function. (*args)
    :param fill: Column names for parameters to be filled using fillna with ffill. (*args)
    :param params: Parameters passed on to the function (**kwargs)
    :returns: a dataframe column for the custom calculated parameter
    """

    if df is None:
        raise Exception('No DataFrame selected.')

    if name == '' or name is None:
        raise Exception('No parameter name defined.')

    if (fn is None):
        raise Exception('No function defined.')

    if hasattr(fn, '__call__'):
        df_tmp = df.sort_values(by=['sample', 'time'], ascending=True)
        if len(fill) > 0:
            print('Column(s) {0} filled.'.format(",".join(fill)))
            # df = df.sort_values(by=['sample', 'time'], ascending=True)
            # df[['fm']] = df[['fm']].fillna(method="ffill")
            df_tmp = df.sort_values(by=['sample', 'time'], ascending=True)
            df_tmp[fill] = df_tmp[fill].fillna(method="ffill")
        for row in df_tmp.sort_values(by=['sample', 'time'], ascending=True).itertuples():
            df_tmp.at[row.Index, name] = fn(
                *[getattr(row, n) for n in cols], **params)
        df[name] = df_tmp[name]
    else:
        raise Exception('No function defined.')
