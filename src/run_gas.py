from experiments.runner import *
from globalParams import *

import sys

#source_path = source_dir + "gas/extracted_gas.out.part2"
source_path = source_dir + "gas/data.csv"


def run_multiple_adam():
    stats, labels = run_multiple(source_path,
                                 [
                                     [
                                         "[AdaM, IS=ARTC" + str(spf) + "]",
                                         udsf.rtta.ARTC(spf, aP, aI, aD, d_init, alpha, beta,
                                                       minIntervalDiameter, 1000, -1),
                                         udsf.rts.AdaM(d_init, alpha, beta, gamma, 1., minStepSize)
                                     ] for spf in [.01, .025, .04, .045, .05, .1, .25]
                                     #] for spf in [.025, .04, .045, .05, .25]
                                 ]
                                 + [
                                     [
                                         "[AdaM,IS=FIXED" + str(p) + "]",
                                         udsf.rtta.Fixed(p),
                                         udsf.rts.AdaM(d_init, alpha, beta, gamma, 1, minStepSize)
                                     ] for p in [0, 5, 155, 220, 360, 475]
                                 ])
    plot_summary(stats[:, 0], stats[:, 1], stats[:, 4], stats[:, 2], stats[:, 5], labels)
    plt.show()
    np.savetxt("out_statistics_gas_adam.csv", stats[:, [2, 0, 1]], header="Diam,m,v", comments='')


def show_trace_adam():
    spf = .2
    fixed = 300

    show_traces([["[AdaM, IS=ARTC" + str(spf) + "]",
                  udsf.rtta.ARTC(spf, aP, aI, aD, d_init, alpha, beta, minIntervalDiameter, 100, -1),
                  udsf.rts.AdaM(d_init, alpha, beta, gamma, 1., minStepSize)],
                 ["[AdaM,IS=FIXED" + str(fixed) + "]",
                  udsf.rtta.Fixed(fixed),
                  udsf.rts.AdaM(d_init, alpha, beta, gamma, 1, minStepSize)]
                 ], source_path, 0, 1, 0, 0, 100000)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        show_trace_adam()
    else:
        run_multiple_adam()
