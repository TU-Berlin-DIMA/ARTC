from data.physical_sensor_log import LoggingSensor

import random


def to_int(floating_point):
    integer = int(floating_point)
    assert(floating_point >= integer)
    return integer + (integer != floating_point and random.random() <= floating_point - integer)


class SensorNode:
    """
    Representation of the sensor node, which, in this simulation, is modelled to only contain
    exactly one sensor with exactly one query.

    During multi query read scheduling, we sample a random value from the read interval in order to
    simulate the multi query optimization with a lot of concurrent queries.
    """

    def __init__(self, sensor, rts_algorithm, is_algorithm, penalty_function, mqrs_simulator):

        self.sensor = LoggingSensor(sensor)

        self.readTimeSuggestionAlg = rts_algorithm
        self.intervalSuggestionAlg = is_algorithm
        self.penaltyFunctionImpl = penalty_function
        self.multiQueryReadSchedulingSimulator = mqrs_simulator

        self.name = ';'.join([self.sensor.sensor.name, rts_algorithm.name, is_algorithm.name, 
                              penalty_function.name, mqrs_simulator.__name__])

        self.experimentFinished = False

    def run(self):
        """ Read from the sensor until the sensor is out of data """
        self.sensor.read(1)
        while not self.experimentFinished:
            self.perform_next_read()

    def perform_next_read(self):
        """
        This algorithm simulates Multi Query Read Scheduling using the proposed solution to 
        adapting interval borders and returns the time and value of the next read.

        @return (t, v)
        """

        # In order to conduct the next sensor read, all queries attached to the physical sensor
        # propose the quadruple <t_s, t_D, t_e, p>. The actual read time is determined by
        # minimizing the penalty functions for the next segment.
        #
        # This simulation does not consider multiple queries, hence, in order to simulate the
        # system under high load, a random value is drawn from the proposed interval [t_s, t_e]
        # around the desired read time t_D according to the penalty function p.
        t_s, t_d, t_e, p = self.__query_tic()
        
        # Simulate the effect of multiple queries on the system
        t_read = self.multiQueryReadSchedulingSimulator(t_s, t_d, t_e, p)
        assert(t_read >= t_s)
        assert(t_read <= t_e)

        # Read the next value from the sensor.
        if self.sensor.sensor.is_almost_finished(t_read - self.sensor.get_current_index()):
            self.experimentFinished = True
            return 0

        self.sensor.read(t_read-self.sensor.get_current_index(),
                         t_d-self.sensor.get_current_index(), t_s, t_e)
        return t_read, self.sensor.get_current_value()

    def __query_tic(self):
        """
        After a value was read from one sensor, the suggestions concerning the next read for all
        queries attached to that sensor have to be updated.

        This function does this for one query, and returns the 
        interval boundaries t_s and t_e, next desired read time t_D, and the penalty function
        p: [t_s, t_e] -> \\R^2 in the following order:
        t_s, t_D, t_e, p

        @return 
        """
        # Suggest the next desired read time, based on the last sensor read time 
        # (self.sensor.get_current_index()) and the last sensor read.
        t_d = self.readTimeSuggestionAlg.next(self.sensor.get_current_index(),
                                              self.sensor.get_current_value())
        assert(t_d > self.sensor.get_current_index())

        # produce interval diameter, and compute interval start and end points
        self.intervalSuggestionAlg.next(self.sensor.get_current_index(),
                                        self.sensor.get_current_value(), t_d)
        t_s = to_int(self.intervalSuggestionAlg.t_s)
        t_e = to_int(self.intervalSuggestionAlg.t_e)
        assert(t_e >= t_s)
        assert(t_s > self.sensor.get_current_index())

        # Generate the new penalty function
        p = self.penaltyFunctionImpl.next(t_s, t_d, t_e, self.sensor.get_current_index(),
                                          self.sensor.get_current_value())
        return t_s, t_d, t_e, p



