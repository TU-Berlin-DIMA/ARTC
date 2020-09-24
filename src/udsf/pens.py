# Penalty function algorithms

import numpy as np


class PenaltyFunctionGenerator:
    def __init__(self):
        self.name = str(list(zip(locals().keys(), locals().values())))

    def next(self, t_s, t_d, t_e, t, v):
        raise NotImplementedError("next(...) not implemented.")


class UniformPenalty:
    def __init__(self):
        self.name = str(list(zip(locals().keys(), locals().values())))

    def next(self, t_s, t_d, t_e, t, v):
        return np.ones(t_e - t_s + 1)

