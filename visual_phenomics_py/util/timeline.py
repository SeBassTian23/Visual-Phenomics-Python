"""
Build timeline for standard protocol
"""

import numpy as np

def protocol_std_timing(offset=0, hours=16, protocol=None, header=False):
    """Generate timing columns for standard DEPI protocols

    Generate the measurement times for a standard DEPI protocol. The available protocols are for a flat day
    with 1 measurement per hour, a sinusoidal day with 2 measurements per hour and a fluctuating day with
    4 measurements per hour. The dark protocol is only producing one measurement at the beginning of the day.

    :param offset: Offset in hours (default: 0)
    :param hours: Hours measured per day (default: 16)
    :param protocol: Measurement Protocol (dark, flat, sinusoidal, fluctuating)
    :param header: Include the first column "name[position][flat][experiment][camera][replicate]" (default: False)
    """

    if protocol is None:
        raise Exception(
            'Protocol type needs to be selected (dark, flat, sinusoidal, fluctuating).')

    if protocol not in ['dark', 'flat', 'sinusoidal', 'fluctuating']:
        raise Exception(
            'Unknown protocol, select: dark, flat, sinusoidal or fluctuating.')

    if not isinstance(header, bool):
        raise Exception(
            'Header needs to be boolean (True or False).')

    timing = []

    if protocol == 'dark':
        timing = np.array([0]) + offset

    if protocol == 'flat':
        steps = hours
        stepsize = hours/steps
        timing = np.arange(stepsize, hours+stepsize, (hours/steps)) + offset

    if protocol == 'sinusoidal':
        steps = hours * 2
        stepsize = hours/steps
        timing = np.arange(stepsize, hours+stepsize, (hours/steps)) + offset

    if protocol == 'fluctuating':
        steps = hours * 4
        stepsize = hours/steps
        stepsize = (hours/steps)
        duration = 0.0833
        timing = np.arange(stepsize, hours+stepsize, (hours/steps)).tolist()
        timing = [x + duration if x in timing[0::2] else x for x in timing]
        timing = np.array(timing) + offset

    timing = timing.astype(float)
    if header:
        timing = ['name[position][flat][experiment][camera][replicate]'] + timing.tolist()
    return timing
    