import math


class Pewma:

    def __init__(self, p_d_init, p_alpha, p_beta):

        self.p_d_init = p_d_init
        self.p_alpha = p_alpha
        self.p_beta = p_beta

        self.count = 0
        self.est_var = float('nan')
        self.est_mean = float('nan')

        self.s1 = 0
        self.s2 = 0

        assert(self.p_d_init >= 2)

    def next(self, delta_i):
        delta_i = float(delta_i)

        if self.count == 0:
            self.s1 = delta_i
            self.s2 = delta_i**2

            self.est_var = 0
            self.est_mean = delta_i

        else:
            if self.count < self.p_d_init:
                p_a = 1 - 1. / self.p_d_init  # XXX: different in java code. PEWMA.java, l25.
            else:
                z = -((delta_i-self.est_mean)/self.est_var)**2 if self.est_var > 0 else 0.
                p_p = 1. / math.sqrt(2.*math.pi) * math.exp(z)**2 / 2.
                p_a = self.p_alpha * (1. - self.p_beta * p_p)
                
            self.s1 = p_a * self.s1 + (1.-p_a) * delta_i
            self.s2 = p_a * self.s2 + (1.-p_a) * delta_i**2

        self.est_mean = self.s1
        assert(self.s2 - self.s1**2 >= -.1)  # might not be the case by a slim margin due to rounding errors.
        self.est_var = math.sqrt(max(self.s2 - self.s1**2, 0))
        assert(self.est_var >= 0)
        
        self.count = self.count + 1
        return self.est_mean



