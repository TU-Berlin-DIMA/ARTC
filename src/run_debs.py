from experiments.runner import *
from globalParams import *

import sys


source_path = source_dir + "football/data.csv"


def run_multiple_adam():
    stats, labels = run_multiple(source_path,
                                 [
                                     [
                                         "[AdaM, IS=2; " + str(spf) + "]",
                                         udsf.rtta.ARTC(spf, aP, aI, aD, d_init,
                                                       alpha, beta, minIntervalDiameter, 10000, -1),
                                         udsf.rts.AdaM(d_init, alpha, beta, gamma, 1., minStepSize)
                                     ] for spf in [0.01, .025, .05, .1, .25, .4]
                                 ]
                                 + [
                                     [
                                         "[AdaM,IS=FIXED" + str(p) + "]",
                                         udsf.rtta.Fixed(p),
                                         udsf.rts.AdaM(d_init, alpha, beta, gamma, 1, minStepSize)
                                     ] for p in [0, 0.35, 0.47, 0.5, 1.15, 2.5, 4.3]
                                 ])
    plot_summary(stats[:, 0], stats[:, 1], stats[:, 4], stats[:, 2], stats[:, 5], labels)
    plt.show()
    np.savetxt("out_statistics_debs_adam.csv", stats[:, [2, 0, 1]], header="Diam,m,v", comments='')


def show_trace_adam():
    spf = .02
    show_traces([["[AdaM, IS=2; " + str(spf) + "]",
                  udsf.rtta.ARTC(spf, aP, aI, aD, d_init, alpha, beta, minIntervalDiameter, 10000, -1),
                  udsf.rts.AdaM(d_init, alpha, beta, gamma, 1., minStepSize)]
                 ], source_path, 0, 1, 0, 0, 6500000)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        show_trace_adam()
    else:
        run_multiple_adam()
