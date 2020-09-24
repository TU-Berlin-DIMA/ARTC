# This file contains functions to plot statistics over one or multiple conducted experiments.

from matplotlib import pyplot as plt
import numpy as np


figsize = (15, 6)
linewidth = 2


def flatten(l):
    return [item for sublist in l for item in sublist]


def plot_summary(error_means, error_vars, p_error_exceeds_threshold, interval_len_means,
                 reads, labels):

    plot_inflicted_error = True
    plot_interval_diameter = True
    plot_conducted_reads = False

    amount_plots = plot_inflicted_error + plot_interval_diameter + plot_conducted_reads
    pid = 1

    if plot_inflicted_error:
        sp = plt.subplot(amount_plots, 1, pid)
        pid += 1
        sp.title.set_text("error")
        x = np.arange(error_means.shape[0])
        plt.errorbar(x, error_means, yerr=error_vars ** 2, fmt='o', label="inflicted error")

    if plot_interval_diameter:
        sp = plt.subplot(amount_plots, 1, pid)
        pid += 1
        sp.title.set_text("Proposed Interval diameter")
        plt.bar(np.array(labels).astype("str"), interval_len_means, color="grey",
                label="interval length")
        plt.legend()

    if plot_conducted_reads:
        sp = plt.subplot(amount_plots, 1, pid)
        pid += 1
        sp.title.set_text("Total conducted reads")
        plt.bar(np.array(labels).astype("str"), reads, color="red", label="total conducted reads")
        plt.legend()


def plot_adam_stats(data, adam):

    plt.subplot(2, 1, 1)

    y = adam.get_log_mean()
    e = adam.get_log_var()
    e = (e > 0) * e
    err = (e < 0) * e
    x = adam.get_log_td()
    plt.plot(x, y, 'k-', c=(0, 0, 1, .4), linewidth=linewidth, label="PEWMA est: error mean & var")
    plt.fill_between(x, y-e, y+e, color=(0, 0, 1, .2), label="sigma")
    plt.fill_between(x, y-err, y+err, color=(1, 0, 0, .4), label="rounding error")

    plt.scatter(np.arange(data.shape[0]), data, s=100, c="black", marker='x', label="original data")
   
    plt.scatter(x, data[x.astype("int")], s=100, c="red", marker='x', label="original data")
    plt.xlim([0, np.max(x)])
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(x, adam.get_log_confidence(), 'k-', c=(0, 0, 1, .4), linewidth=linewidth, 
             label="confidence")
    plt.xlim([0, np.max(x)])
    plt.legend()
    plt.show()


def plot_estimates(data, y, e, name, offset, label=False, fill=False, show=False):
    x = np.arange(offset, offset + data.shape[0])
    kwargs = {"label": "original data"} if label else {}

    if len(data.shape) > 1:
        for i in range(data.shape[1]):
            plt.scatter(x, data[:, i], s=25, marker='x', **kwargs)
        return
    plt.scatter(x, data, s=25, c="black", marker='x', **kwargs)

    do_zip = False
    # zX = flatten(list(zip(x, x+.99))) if do_zip else x
    # zData = flatten(list(zip(data, data))) if do_zip else data
    # zY = flatten(list(zip(y, y))) if do_zip else y

    if len(e.shape):
        kwargs = {"label": "estimate +- sigma"} if label else {}
        plt.fill_between(x, y-e, y+e, color=(0, 0, 1, .2), **kwargs)

    if fill:
        kwargs = {"label": "[estimate:value]"} if label else {}
        plt.fill_between(x, y, data, color=(1, 0, 0, .4), **kwargs)

    plt.legend()


def plot_trace(sensor, name, plot_error=True, plot_error_sum=True, plot_read_diam=True,
               val1=0, val2=-1, show=True):
    plot_traces([[sensor, "", None]], name, plot_error, plot_error_sum, plot_read_diam, val1, val2, show)


def plot_traces(sensors, name, plot_error=True, plot_error_sum=True, plot_read_diam=True,
                val1=0, val2=-1, show=True):

    plot_additional_rtta = 1
    # plot_additional_rtta = 3

    amount_plots = plot_error + plot_read_diam + plot_error_sum + 1 + plot_additional_rtta
    plot_number = 1
    plt.figure(figsize=[figsize[0] * 1, figsize[1] * amount_plots])
    plt.suptitle(name)

    min_amount_samples = -1
    for _, (sensor, _, _) in enumerate(sensors):
        min_amount_samples = min(sensor.get_current_index(), min_amount_samples) \
                             if min_amount_samples >= 0 else sensor.get_current_index()
    val2 = min_amount_samples if val2 == -1 else min(min_amount_samples, val2)
    val1 = min(val1, val2)

    if plot_error:
        sp = plt.subplot(amount_plots, 1, plot_number)
        sp.title.set_text("cumulative error")
        cmap = plt.cm.get_cmap("hsv", len(sensors))
        x = np.arange(val1, val1 + val2 - val1)
        header = "x, "
        xx = x - val1
        for cid, (sensor, label, _) in enumerate(sensors):
            ie = sensor.get_error_ratio()[val1:val2]
            y = np.add.accumulate(ie / ie.shape[0])
            plt.plot(x, y, linewidth=linewidth, label=label)
            xx = np.vstack((xx, y))
            header += label.replace(',', ";") + ","
        np.savetxt("tmpSinglePlotErr.csv", xx.T, delimiter=",", header=header)
        plt.legend()
        plot_number += 1

    if plot_error_sum:
        sp = plt.subplot(amount_plots, 1, plot_number)
        sp.title.set_text("moving average error")
        sp.set_ylabel("moving average of |estimated value - observed value| / |mean(value)|")
        sp.set_xlabel("experiment time")
        cmap = plt.cm.get_cmap("hsv", len(sensors))
        diam2 = 25
        diam = 0
        x = np.arange(val1, val1 + val2 - val1)
        header = "x, "
        xx = x - val1
        for cid, (sensor, label, _) in enumerate(sensors):
            ie = sensor.get_error_ratio()[val1:val2]
            # y = np.array([np.mean(ie[max(em-diam, 0):min(em+diam+1, ie.shape[0])]) \
            #               for em in range(ie.shape[0])])
            yd = np.array([np.mean(ie[max(em-diam2, 0):min(em+diam2+1, ie.shape[0])])
                           for em in range(ie.shape[0])])
            # plt.scatter(np.arange(val1, val1 + y.shape[0]), y, label=label, s=.33, color="red")
            plt.plot(x, yd, linewidth=linewidth, label=label)
            xx = np.vstack((xx, yd))
            header += label.replace(',', ";") + ","
        np.savetxt("tmpSinglePlotErrSum.csv", xx.T, delimiter=",", header=header)
        plt.legend()
        plot_number += 1

    # interval diameter suggestion (custom)
    if plot_additional_rtta:

        sp = plt.subplot(amount_plots, 1, plot_number)
        sp.title.set_text("diam")
        for _, _, rtta in sensors: 
            if hasattr(rtta, "pdm"):
                nptm = np.array(rtta.ptm)
                cond = ((nptm >= val1) * ((nptm <= val2) if val2 != -1 else 1))
                x = nptm[cond]
                y = np.array(rtta.ppd)[cond]
                plt.plot(x, y, linewidth=linewidth, label="ppd")
                np.savetxt("tmpSinglePlotDiam.csv", np.vstack((x - val1, y)).T, delimiter=",", 
                           header="x, diam")
        plt.legend()
        plot_number += 1
       
        if plot_additional_rtta > 1:
            sp = plt.subplot(amount_plots, 1, plot_number)
            sp.title.set_text("shift")
            for _, _, rtta in sensors: 
                if hasattr(rtta, "pdm"):
                    nptm = np.array(rtta.ptm)
                    cond = ((nptm >= val1) * ((nptm <= val2) if val2 != -1 else 1))
                    if cond.shape[0]:
                        x = nptm[cond]
                        y = np.array(rtta.pps)[cond]
                        plt.plot(x, y, linewidth=linewidth, label="ppd")
                        np.savetxt("tmpSinglePlotShift.csv", np.vstack((x - val1, y)),
                                   delimiter=",", header="x, shift")
            plt.legend()
            plot_number += 1

        if plot_additional_rtta > 2:
            sp = plt.subplot(amount_plots, 1, plot_number)
            sp.title.set_text("PEWMA diff mean")
            for _, _, rtta in sensors:
                if hasattr(rtta, "pdm"):
                    nptm = np.array(rtta.ptm)
                    cond = ((nptm >= val1) * ((nptm <= val2) if val2 != -1 else 1))

                    plt.plot(nptm[cond], np.array(rtta.pdm)[cond], linewidth=linewidth, label="mean")
                    plt.plot(nptm[cond], np.array(rtta.pdv)[cond], linewidth=linewidth, label="var")
            plt.legend()
            plot_number += 1

    if plot_read_diam:
        sp = plt.subplot(amount_plots, 1, plot_number)
        sp.title.set_text("Read Deltas")

        for sensor, label, _ in sensors:
            rtta = sensor.get_read_deltas()
            x = np.arange(sensor.get_current_index()+1)
            y = np.zeros(sensor.get_current_index()+1)
            l = 0
            for i in rtta:
                i = int(i)
                y[l:l+i] = i
                l += i

            plt.plot(x[val1:val2], y[val1:val2], linewidth=linewidth, label=label)
        plot_number += 1

    sp = plt.subplot(amount_plots, 1, plot_number)
    sp.title.set_text("Experiment Trace")
    sp.set_xlabel("experiment time")
    sp.set_ylabel("sensor value")

    for en, (sensor, label, _) in enumerate(sensors):
        rt = sensor.get_read_times().astype("int")
        rt = rt[(rt >= val1) * ((rt <= val2) + (val2 == -1))]
        if rt.shape[0] > 0:
            do_zip = True
            y = sensor.get_observed_data()[rt]
            y = np.array(flatten(list(zip(y, y))) if do_zip else y)
            rt = np.array(flatten(list(zip(rt, list(rt[1:]) + [rt[-1]]))) if do_zip else rt)
            if en != 2:
                plt.plot(rt, y, linewidth=1.5, alpha=.7, label=label)
                np.savetxt("tmpSinglePlotApprox" + str(en) + ".csv",
                           np.vstack((rt - val1, y.T)).T, delimiter=",", header="x" + label)

            plot_estimates(sensor.get_available_data()[val1:val2],
                           sensor.get_observed_data()[val1:val2], np.array(0),
                           "out/test/testAdam.png", val1, en == 0, False, show)
        if en == 0:
            np.savetxt("tmpSinglePlotData.csv", np.vstack((np.arange(val2-val1),
                       sensor.get_available_data()[val1:val2].T)).T, delimiter=",", header="x,y")

    if show:
        plt.show()
