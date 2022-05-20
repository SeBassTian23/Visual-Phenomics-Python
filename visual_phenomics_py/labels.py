"""
Export data from the DataFrame into the Visual Phenomics 
text file format
"""

LABELS_FORMATTED = {
  'f0': r'$F_{0}$',
  'fm': r'$F_{M}$',
  'fmp': r'$F_{M}\'$',
  'fmpp': r'$F_{M}\'\'$',
  'fmt': r'$F_{Mt}$',
  'fs': r'$F_{S}$',
  'fvfm': r'$\frac{F_{V}}{F_{M}}$',
  'light_intensity': r'PAR [$\mu mol$ $photons \times m^{-2} \times s^{-1}$]',
  'name': 'Strain',
  'npq': r'$NPQ$',
  'npqt': r'$NPQ_{t}$',
  'phi2': r'$\Phi_{II}$',
  'phino': r'$\Phi_{NO}$',
  'phinot': r'$\Phi_{NOt}$',
  'phinpq': r'$\Phi_{NPQ}$',
  'phinpqt': r'$\Phi_{NPQt}$',
  'qe': r'$q_{E}$',
  'qesv': r'$q_{ESV}$',
  'qet': r'$q_{Et}$',
  'qi': r'$q_{I}$',
  'qit': r'$q_{It}$',
  'ql': r'$q_{L}$',
  'qlt': r'$q_{Lt}$',
  'time': r'Time [h]',
}

def label( param='', additional={} ):
  """Return formated string

  Return a formatted string for a column name if available.
  In case a formatted label is not found, the input is returned.

  :param param: provided column name
  :param additional: dictionary with additional formatted strings. Overwrites an existing defined format.
  :returns: 'formatted label' (string)
  """
  if param in LABELS_FORMATTED:
    if param in additional:
      return additional[param]
    return LABELS_FORMATTED[param]
  elif param in additional:
    return additional[param]
  else:
    return param
