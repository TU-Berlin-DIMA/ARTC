# This file contains global parameters, that are used in the run_* python scripts in order to
# configure AdaM, PEWMA or ARTC

######################### Configuration of utilities used by AdaM / ARTC ##########################
# PID controller: proportional, integral, and differential gain
aP, aI, aD = 2, .002, .3
# PEWMA: Factors alpha (cmp. EWMA) and beta (factor with which PDF is multipled)
alpha, beta = 0.5, .6
# PEWMA: Initialization period of PEWMA in [#samples], during which parameters of the probability
#        distribution are learned and EWMA is executed .
d_init = 20

############################# Configuration of specific UDSF components ###########################
# IDS: minimal interval diameter that can be proposed by the interval suggestion algorithm:
minIntervalDiameter = 1
# RTS: minimal step size that is allowed by the read time suggestion algorithm:
minStepSize = 1

# Configuration of AdaM
gamma = 0.2

############################## Configuration the execution environment #############################
# root data-source directory of the data. If evoked as described in the README, the default is fine.
source_dir = "data/"
# Amount of iterations to be performed for each configuration of a multi-execution experiment.
amount_iterations = 1
amount_iterations = 10

# Amount of samples used from the dataset (can be used to speed up the experiments to a certain
# extent)
# Attention: When using `max_amount_samples != -1`, the configuration of the fixed algorithm might
#            not match those of ARTC in the enabled extent of read-sharing potential)
max_amount_samples = 100000
max_amount_samples = -1
