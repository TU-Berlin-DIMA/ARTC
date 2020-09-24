# Contains read time suggestion algorithms

from util.pewma import Pewma

import math
import numpy as np


class ReadTimeSuggestionAlgorithm:
    """  Read time suggestion dummy class. """

    def next(self, t, v): raise NotImplementedError("next(...) not implemented.")


class Periodic(ReadTimeSuggestionAlgorithm):
    """ Suggest read time using a fixed distance between consecutive read times. """

    def reset(self):
        pass

    def __init__(self, dt):
        self.name = str(list(zip(locals().keys(), locals().values())))
        self.dt = dt

    def next(self, t, v): return round(t + self.dt)


class AdaM(ReadTimeSuggestionAlgorithm):
    """ AdaM read time suggestion algorithm.  """

    def reset(self):
        self.pewma = Pewma(self.p_d_init, self.p_alpha, self.p_beta)
        self.v_last = float('nan')
        self.conf = float('nan')
        self.logMean = np.empty([self.logSize])
        self.logVar = np.empty([self.logSize])
        self.logConf = np.empty([self.logSize])
        self.logTD = np.empty([self.logSize])
        self.iterationNumber = 0

    def __init__(self, p_d_init, p_alpha, p_beta, p_gamma, p_lambda, p_t_min, log_size=0):
        self.name = str(list(zip(locals().keys(), locals().values())))
        self.p_d_init = p_d_init
        self.p_alpha = p_alpha
        self.p_beta = p_beta
        self.p_gamma = p_gamma
        self.p_lambda = p_lambda
        self.p_T_min = p_t_min
        self.logSize = log_size

        assert (self.p_gamma < 1)
        assert (self.p_gamma > 0)

        self.reset()

    def __has_sample(self):
        return not np.isnan(self.v_last).all()

    def next(self, t, v):
        if self.__has_sample():
            delta_i = np.sum(np.abs(self.v_last - v))

            prev_variance = self.pewma.est_var
            self.pewma.next(delta_i)
            curr_variance = self.pewma.est_var

            self.conf = 1. - (0 if prev_variance == 0 else math.fabs(curr_variance - prev_variance) / prev_variance)
            self.conf = max(self.conf, 0)  # XXX: neither in paper, nor in java implementation, but makes sense.

            if self.conf >= 1 - self.p_gamma:
                self.td_next = round(self.td_next + self.p_lambda * (
                            1. + math.fabs(self.conf - self.p_gamma) / self.conf))  # XXX: fabs due to AdaM:53
            else:
                self.td_next = self.p_T_min
        else:
            self.td_next = self.p_T_min

        assert (self.td_next >= self.p_T_min)
        t_d = round(t + self.td_next)

        if self.iterationNumber < self.logMean.shape[0]:
            self.logMean[self.iterationNumber] = self.pewma.est_mean
            self.logVar[self.iterationNumber] = self.pewma.est_var
            self.logConf[self.iterationNumber] = self.conf
            self.logTD[self.iterationNumber] = t_d

        self.iterationNumber += 1
        self.v_last = v

        return t_d

    def get_log_mean(self):
        return self.logMean[:self.iterationNumber - 1]

    def get_log_var(self):
        return self.logVar[:self.iterationNumber - 1]

    def get_log_confidence(self):
        return self.logConf[:self.iterationNumber - 1]

    def get_log_td(self):
        return self.logTD[:self.iterationNumber - 1]
