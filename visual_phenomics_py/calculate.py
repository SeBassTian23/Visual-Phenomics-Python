"""
Calculate additional parameters or recalculate parameters.
"""

from numpy import nan

def phi2_phinpq_ideal(qL, Phi2, PhiNO, PhiNO_opt = 0.25):
  """
  Calculate ideal Phi2 and PhiNPQ from a fluorescence measurement based on qL, Phi2 and PhiNO.

  :param qL: Measured qL
  :param Phi2: Measured Phi2
  :param PhiNO: Measured Phi2
  :param PhiNO_opt: The optimum PhiNO value (default: 0.25)
  :returns: a list with Phi2 ratio, ideal Phi2, ideal PhiNPQ, delta NPQ
  """

  Phi2_0_Phi2_2 = 1+ Phi2 * (1/PhiNO_opt - 1/PhiNO)/ (qL  * 4.88) 
  
  Phi2_2_Phi2_0 = 1/Phi2_0_Phi2_2

  Phi2_ideal = Phi2 * Phi2_2_Phi2_0
  PhiNPQ_ideal = 1 - (Phi2_ideal + 0.2)
  delta_NPQ = 1/0.2 - 1/PhiNO

  return [Phi2_2_Phi2_0, Phi2_ideal, PhiNPQ_ideal, delta_NPQ]

def calculate_ideal_parameters(df=None, phi2='phi2', phino='phino', qL='ql', phino_opt = 0.25):
  """
  Calculate ideal Phi2 and PhiNPQ from a fluorescence measurement based on qL, Phi2 and PhiNO.

  :param df: The DataFrame to add the calculated parameters to.
  :param qL: Measured qL
  :param Phi2: Measured Phi2
  :param PhiNO: Measured Phi2
  :param PhiNO_opt: The optimum PhiNO value (default: 0.25)
  :returns: a list with Phi2 ratio, ideal Phi2, ideal PhiNPQ, delta NPQ
  """

  if df is not None:
    df['Vx'] = df[phino] * 0.5 * (1-df[qL])
    df['Phi2 - ideal']   = nan
    df['PhiNPQ - ideal'] = nan
    df['Delta NPQ']      = nan
    df['Phi2 - ratio']   = nan

    for idx,row in df[[phi2,qL,phino]].dropna().iterrows():
      phi2ratio, phi2_ideal, phinpq_ideal, delta_npq = phi2_phinpq_ideal(row[qL],row[phi2],row[phino], 0.25)

      df.loc[idx,'Phi2 - ideal']   = phi2_ideal
      df.loc[idx,'PhiNPQ - ideal'] = phinpq_ideal
      df.loc[idx,'Delta NPQ']      = delta_npq
      df.loc[idx,'Phi2 - ratio']   = phi2ratio

  else:
    print('No DataFrame selected.')

def calculate():
  # Fvfm        (fm - f0) / fm
  # Npq         (fm - fmp) / fmp
  # Npqt        (4.88 / ((fmp / f0p) - 1)) - 1
  # Phi2        (fmp - fs) / fmp
  # Phino       1 / (npqt + (1 + (ql * 8.88)))
  # Phinpq      1 - phi2 - phiNo
  # Qe          (fmpp - fmp) / fmp
  # Qesv        (fm / fmp) - (fm / fmpp)
  # Qet         npqt - qit
  # Qi          (fm - fmpp) / fmpp
  # Qit         (4.88 / ((fmpp / f0pp) - 1)) - 1
  # QI          ((fmp - fs) / (fmp - f0p)) * (f0p / fs)
  print("Not implemented yet")
