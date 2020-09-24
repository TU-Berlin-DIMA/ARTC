from experiments.runner import *
from globalParams import *

import sys


def run_multiple_adam():
    source_path = source_dir + "activities/data.csv"

    stats, labels = run_multiple(source_path,
                                 [
                                     [
                                         "[AdaM, IS=ARTC" + str(spf) + "]",
                                         udsf.rtta.ARTC(spf, aP, aI, aD, d_init, alpha, beta,
                                                       minIntervalDiameter, 175, -1),
                                         udsf.rts.AdaM(d_init, alpha, beta, gamma, 1., minStepSize)
                                     ] for spf in [.01, .1, .2, .25, .3, .35, .4]
                                 ]
                                 + [
                                     [
                                         "[AdaM,IS=Fixed" + str(p) + "]",
                                         udsf.rtta.Fixed(p),
                                         udsf.rts.AdaM(d_init, alpha, beta, gamma, 1, minStepSize)
                                     ] for p in [0, 3.3, 6, 10, 15, 20, 29.2, 37]
                                 ])
    plot_summary(stats[:, 0], stats[:, 1], stats[:, 4], stats[:, 2], stats[:, 5], labels)
    plt.show()
    np.savetxt("out_statistics_activities_adam.csv", stats[:, [2, 0, 1]], header="Diam,m,v",
               comments='')


def show_trace_adam():
    source_path = source_dir + "activities/small.csv"

    show_traces([["[AdaM,         Fixed ] ",
                  udsf.rtta.Fixed(10),
                  udsf.rts.AdaM(d_init, alpha, beta, 0.1, 1, minStepSize)],
                 ["[AdaM,          ARTC] ",
                  udsf.rtta.ARTC(.05, aP, aI, aD, d_init, alpha, beta, 0, 175, -1),
                  udsf.rts.AdaM(d_init, alpha, beta, 0.1, 1., minStepSize)],
                 ["[AdaM,          Fixed ] ",
                  udsf.rtta.Fixed(0),
                  udsf.rts.AdaM(d_init, alpha, beta, 0.1, 1, minStepSize)],
                 ], source_path, 0, 1, 0, 2300, 3200)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        show_trace_adam()
    else:
        run_multiple_adam()
