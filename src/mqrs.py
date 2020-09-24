# Contains simulators for Multi-Query Read-Scheduling

import random
import numpy as np


# Statistics of the multi-query read-scheduling that are logged on-the-fly in a circular buffer.
mqrsIndex = 0
mqrsStatsSamplingPosition = np.empty([10000])
mqrsStatsFull = False


def select_rand(t_s: int, t_d: int, t_e: int, p: np.array) -> int:
    """!
    Simulate Multi Query Read Scheduling by sampling uniformly on the proposed interval;
    independent on the penalty function.

    :param t_s: int
                start time of the interval [t_s, t_e]
    :param t_d: int
                desired read time within the interval [t_s, t_e]
    :param t_e: int
                end time of the interval [t_s, t_e]
    :param p:   np.array([t_e  - t_s])
    :return:    the next read time on [t_s, t_e]
    """
    assert(t_s <= t_d <= t_e)
    assert(len(p.shape) == 1 and p.shape[0] == t_e - t_s + 1)
    assert((p > 0).all())
    val: int = random.randint(t_s, t_e)
    assert (t_s <= val <= t_e)
    log_stats(val, t_s, t_e)

    return val


def select_rand_pen(t_s: int, t_d: int, t_e: int, p: np.array) -> int:
    """ 
    Simulate Multi Query Read Scheduling by sampling at random according to the inverse of the
    penalty function.

    @see selectRand
    :param t_s: int
                start time of the interval [t_s, t_e]
    :param t_d: int
                desired read time within the interval [t_s, t_e]
    :param t_e: int
                end time of the interval [t_s, t_e]
    :param p:   np.array([t_e  - t_s])
    :return:    the next read time on [t_s, t_e]
    """
    assert(t_s <= t_d <= t_e)
    assert(len(p.shape) == 1 and p.shape[0] == t_e - t_s + 1)
    assert((p > 0).all())
    val: int = random.choices(np.arange(t_s, t_e + 1), weights=1./p)[0] if t_s < t_e else t_s
    assert (t_s <= val <= t_e)
    log_stats(val, t_s, t_e)

    return val


def get_stats_sampling_position():
    """
    :return:  the mqrs statistics on the selected values on UDSFs as it is logged.
    """
    return mqrsStatsSamplingPosition[:mqrsStatsSamplingPosition.shape[0] if mqrsStatsFull else mqrsIndex]


def log_stats(val: int, t_s: int, t_e: int):
    """
    Log statistics on the selected value within the interval in order to make sure that everything
    is implemented correctly.

    :param val: int
                selected value \\in [t_s, t_e]
    :param t_s: int
                start time of the interval [t_s, t_e]
    :param t_e: int
                end time of the interval [t_s, t_e]
    """
    if t_e > t_s:
        global mqrsIndex, mqrsStatsSamplingPosition, mqrsStatsFull
        percentage = 1.0 * (val - t_s) / (t_e - t_s)
        mqrsStatsSamplingPosition[mqrsIndex] = percentage
        mqrsIndex += 1
        if mqrsIndex == mqrsStatsSamplingPosition.shape[0]:
            mqrsIndex = 0
            mqrsStatsFull = True


