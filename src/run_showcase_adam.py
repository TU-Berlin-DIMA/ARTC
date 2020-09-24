# This file contains test code in order to showcase traces of some of the implemented algorithms.

from udsf.rts import *
from data.physical_sensor import Sensor
from data.physical_sensor_log import LoggingSensor
from util.plot import *

from matplotlib import pyplot as plt
import numpy as np
import random

random.seed(1)

d_init = 5
alpha = 0.6
beta = 1
gamma = .2
lam = 1 
T_min = 1


def test_adam(input_data, show=True):
    sensor = LoggingSensor(Sensor(str(input_data), input_data))
    sensor.read(1)
    
    adam = AdaM(d_init, alpha, beta, gamma, lam, T_min, input_data.shape[0])

    t_d = 1
    while not sensor.sensor.is_almost_finished(t_d - sensor.get_current_index()):
        sensor.read(t_d-sensor.get_current_index())
        t_d = adam.next(sensor.get_current_index(), sensor.get_current_value())
    
    plt.figure(figsize=figsize)
    plt.clf()
    plot_adam_stats(sensor.get_available_data(), adam)

    plot_trace(sensor, "test_adam.png", show)


def test_pewma(input_data, show=False):

    pewma = Pewma(d_init, alpha, beta)
    estimates = np.array([[pewma.next(i), pewma.est_var] for i in input_data])
    y, e = estimates.T
    
    plt.figure(figsize=figsize)
    plt.clf()
    plot_estimates(input_data, y, e, "test_pewma.png", True, show)
    plt.show()


if __name__ == "__main__":

    # Test with a sin-curve that is not shifted but stretched a little. This is a worst-case
    # scenario for an adaptive read scheduler like adam, as the variability of the data changes
    # quickly and periodically.
    x = np.arange(100)
    data = np.sin(x / np.pi) * x
    data = np.hstack((data, np.sin(np.arange(100, 200) / np.pi) * 100))

    # test pewma on the original data
    test_pewma(data, True)
    
    # test AdaM and the error-pewma
    test_adam(data, True)
