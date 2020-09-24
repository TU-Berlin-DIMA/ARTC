# Contains read interval (diameter) suggestion algorithms

from util.PID import PID
from util.pewma import Pewma

from math import *
import numpy as np


class IntervalSuggestion:
    def __init__(self):
        pass

    def next(self, time, value, t_d):
        raise NotImplementedError("next(...) not implemented.")


class Fixed(IntervalSuggestion):

    def reset(self): pass

    def __init__(self, dur):
        super().__init__()
        assert(dur >= 0)
        self.name = str(list(zip(locals().keys(), locals().values())))
        self.dur = dur
        self.t_s = 0
        self.t_e = 0

    def next(self, time, value, t_d):
        self.t_s = max(t_d - self.dur, time + 1)
        self.t_e = max(t_d + self.dur, time + 1)


class ARTC(IntervalSuggestion):

    def reset(self):
        self.vLast = float('nan')
        self.pidMean = PID(self.setPoint, self.P, self.I, self.D)
        self.pidVar = PID(self.setPoint, self.P, self.I, self.D)
        self.pewma = Pewma(self.d_init, self.alpha, self.beta)
        self.pewmaDiff = Pewma(self.d_init, self.alpha, self.beta)
        self.ptm = []
        self.pdm = []
        self.pdv = []
        self.ppd = []
        self.pps = []

        self.diam = self.minDiam
        self.shift = 0.

    def __init__(self, set_point, p_p, p_i, p_d, d_init, alpha, beta, diam_min, diam_max, avg=-1):
        super().__init__()
        self.name = str(list(zip(locals().keys(), locals().values())))

        self.setPoint = set_point
        self.P = p_p
        self.I = p_i
        self.D = p_d
        self.d_init = d_init 
        self.alpha = alpha
        self.beta = beta

        self.minDiam = diam_min
        self.maxDiam = diam_max

        self.avg = avg

        self.reset()

    def __has_sample(self): return not np.isnan(self.vLast).all()

    def next(self, t, v, t_d):
        self.pewma.next(np.linalg.norm(v))
        mean = self.pewma.est_mean if self.avg == -1 else self.avg

        if self.__has_sample():
            self.pewmaDiff.next(np.linalg.norm(v - self.vLast))

            pidn = self.pidMean.next(t, self.pewmaDiff.est_mean / fabs(mean))

            if self.pewmaDiff.est_var / mean > self.setPoint:
                self.diam = self.diam * .75
            else:
                self.diam += (self.setPoint - self.pewmaDiff.est_var / mean) / self.setPoint
            
            self.shift = min(max(self.shift + pidn / 10, -.5), .25) 
            self.diam = min(max(self.diam, self.minDiam), self.maxDiam)

            self.t_s = max(t_d + self.diam * (self.shift - .5), t + 1)
            self.t_e = max(t_d + self.diam * (.5 + self.shift), t + 1)
            
            self.ptm += [t]
            self.pdm += [self.pewmaDiff.est_mean]
            self.pdv += [self.pewmaDiff.est_var]
            self.ppd += [self.diam]
            self.pps += [self.shift]

        else:
            self.t_s, self.t_e = max(t_d - 2, t + 1), max(t_d + 1, t + 1)
        self.vLast = v

