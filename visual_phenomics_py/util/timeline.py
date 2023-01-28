"""
Build timeline for standard protocol
"""

import numpy as np

def protocol_std_timing(offset=0, hours=16, protocol=None):
    """Generate timing columns for standard DEPI protocols

    Generate the measurement times for a standard DEPI protocol. The available protocols are for a flat day
    with 1 measurement per hour, a sinusoidal day with 2 measurements per hour and a fluctuating day with
    4 measurements per hour. The dark protocol is only producing one measurement at the beginning of the day.

    :param offset: Offset in hours (default: 0)
    :param hours: Hours measured per day (default: 16)
    :param protocol: Measurement Protocol (dark, flat, sinusoidal, fluctuating)
    """

    if protocol is None:
        raise Exception(
            'Protocol type needs to be selected (dark, flat, sinusoidal, fluctuating).')

    if protocol not in ['dark', 'flat', 'sinusoidal', 'fluctuating']:
        raise Exception(
            'Unknown protocol, select: dark, flat, sinusoidal or fluctuating.')

    timing = []

    if protocol == 'dark':
        timing = np.array([0]) + offset

    if protocol == 'flat':
        steps = hours
        timing = np.arange(0, hours, (hours/steps)) + offset

    if protocol == 'sinusoidal':
        steps = hours * 2
        timing = np.arange(0, hours, (hours/steps)) + offset

    if protocol == 'fluctuating':
        steps = hours * 4
        duration = 0.0833
        timing = np.arange(0, hours, (hours/steps)).tolist()
        timing = [x - duration if x in timing[1::2] else x for x in timing]
        timing = np.array(timing) + offset

    return timing.astype(float)


def vp_file_header(timing=None, initCol=True):
    """Generate header string for Visual Phenomics output file

    Generate the measurement times for a standard DEPI protocol. The available protocols are for a flat day
    with 1 measurement per hour, a sinusoidal day with 2 measurements per hour and a fluctuating day with
    4 measurements per hour. The dark protocol is only producing one measurement at the beginning of the day.

    :param timing: Numpy array with timing information
    :param initCol: Add/ignore the initial column header name (default: True)
    """

    if timing is None:
        raise Exception('Timing must be genereated using "protocol_std_timing" function or a list of float values.')

    if not isinstance(initCol, bool):
        raise Exception('initCol must be boolean (default is True).')

    string = ''

    if initCol:
        string = 'name[position][flat][experiment][camera][replicate] '

    string = string + np.array2string( np.array(timing), separator='  ', formatter={'float_kind':lambda x: "%.3f" % x})[1:-1]

    return string