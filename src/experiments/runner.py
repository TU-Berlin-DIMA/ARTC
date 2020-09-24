from sensor_node import *
from data.physical_sensor import Sensor
from globalParams import amount_iterations

import udsf.pens
import udsf.rts
import udsf.rtta
import mqrs

from util.plot import *

import random

random.seed(1)


def setup_node(rtta, source_path, rs=None):
    # Load dataset into sensor
    s = Sensor(source_path)
    # Read time suggestion
    assert (rs is not None)

    # Penalty function suggestion
    pen_uniform = udsf.pens.UniformPenalty()
    # Simulation of multi-query read-scheduling
    mqrs_sim_uniform = mqrs.select_rand
    # set some values in interval diameter suggestion in case that is needed.  
    rtta.rs = rs
    rtta.pen = pen_uniform
    rtta.mqrs = mqrs_sim_uniform
    rtta.s = s
    # Create node, run and return it.
    node = SensorNode(s, rs, rtta, pen_uniform, mqrs_sim_uniform)
    node.run()
    return node


def run_multiple(source_path, interval_suggestion_algorithms):
    """ 
    Run multiple experiments on nodes instantiated with all of the specified interval suggestion 
    algorithms.

    """
    print(interval_suggestion_algorithms)
    global stats, nodes, labels, amount_iterations
    stats = np.empty([amount_iterations, len(interval_suggestion_algorithms), 6])
    nodes, labels = [], []
    for it in range(amount_iterations):
        for i, value in enumerate(interval_suggestion_algorithms):
            print("Executing configuration", i + 1, "of", len(interval_suggestion_algorithms))
            label, isa, rs = value[0], value[1], (value[2] if len(value) > 2 else None)
            isa.reset()
            rs.reset()

            node = setup_node(isa, source_path, rs)
            stats[it, i] = [node.sensor.get_error_mean(), node.sensor.get_error_var(),
                            node.sensor.get_proposed_interval_diameter_mean(),
                            node.sensor.get_proposed_interval_diameter_var(),
                            node.sensor.get_percentage_error_larger_than(15),
                            node.sensor.amountReadsConducted]

            # nodes = nodes + [node]
            if it == 0:
                labels = labels + [label]

    stats = np.mean(stats, axis=0)
    return stats, labels


def show_traces(isas, source_path, plot_error=1, plot_error_sum=1, plot_read_diam=1,
                val1=0, val2=-1, single=False):
    sensors = []
    title_all = "avg interval diameter; avg error ratio\n"

    for value in isas:
        label, isa, rs = value[0], value[1], (value[2] if len(value) > 2 else None)
        node = setup_node(isa, source_path, rs)
        sensors = sensors + [[node.sensor, label, isa]]
        title = f"{np.mean(node.sensor.get_proposed_interval_diameters()):.4f}" \
                + f", {node.sensor.get_error_mean():.4f} <-" + label + "\n"

        if single:
            plot_traces([node.sensor, label], title + title_all, plot_error, plot_error_sum,
                        plot_read_diam, val1, val2)
        else:
            title_all = title_all + title
    if not single:
        plot_traces(sensors, title_all, plot_error, plot_error_sum, plot_read_diam, val1, val2)


def print_experiment_summary():
    amount_samples = mqrs.get_stats_sampling_position().shape[0]
    if amount_samples:
        print("mqrs mean and variance and amount non-trivial",
              np.mean(mqrs.get_stats_sampling_position()),
              np.var(mqrs.get_stats_sampling_position()), amount_samples)
