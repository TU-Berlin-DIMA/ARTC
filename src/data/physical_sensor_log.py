import numpy as np


class LoggingSensor:
    """ 
    Extension to a physical sensor, which logs internals of the presented algorithms.
    """

    def __init__(self, sensor):
        self.sensor = sensor

        # Values available for evaluation and logging:
        # The view to the dataset provided through adaptive sampling and read sharing.
        self.readData = np.empty(sensor.data.shape)
        # The amount of reads that were actually conducted until now, initialized to -1, as the 
        # first value gets thrown out.
        self.amountReadsConducted = -1
        # Array for logging the read time deltas, recorded in order to subsequently compute
        # statistics on their distribution.
        self.readDeltas = np.empty(sensor.data.shape[0])
        # Array for logging the read times,
        self.readTimes = np.empty(sensor.data.shape[0])
        # adam pewma mean
        self.adamMean = np.empty(sensor.data.shape[0])
        # adam pewma variance
        self.adamVar = np.empty(sensor.data.shape[0])       
        # adam confidence
        self.adamConf = np.empty(sensor.data.shape[0])
        # delta of consecutive desired read times:      t_{D;i} - t_{D;i-1}.
        self.tdDeltas = np.empty(sensor.data.shape[0])
        # Proposed Interval diameters:                  t_{D;i} - t_{D;i-1}.
        self.proposed_interval_diameter = np.empty(sensor.data.shape[0])

    # Read and access last read

    def read(self, index_delta, index_delta_td=0, t_s=0, t_e=0):
        """
        Read next value from sensor, store and return it and adapt the current time.
        :param index_delta:     relative amount of time (= samples) to skip in the array
        :param index_delta_td:  relative amount of time (= samples) to skip until the next desired read time t_D
        :param t_s:             interval start index as global index (not relative to the current time)
        :param t_e:             interval end index as global index (not relative to the current time)
        :return:
        """
        # Conduct the sensor read
        started = self.sensor.is_started()
        last_val = self.sensor.get_current_value() if started else 0
        self.sensor.read(index_delta)

        if started:
            # Update statistics
            self.amountReadsConducted += 1
            self.readDeltas[self.amountReadsConducted] = index_delta
            self.readTimes[self.amountReadsConducted] = self.get_current_index()
            self.tdDeltas[self.amountReadsConducted] = index_delta_td
            self.proposed_interval_diameter[self.amountReadsConducted] = t_e - t_s

            self.readData[self.sensor.get_current_index() - index_delta: self.sensor.get_current_index() + 1] \
                = last_val

    def get_current_value(self):
        return self.sensor.get_current_value()

    def get_current_index(self):
        return self.sensor.get_current_index()

    # Obtain statistics (in the correct size)

    def get_available_data(self):
        return self.sensor.data[:self.sensor.get_current_index() + 1]

    def get_observed_data(self):
        return self.readData[:self.sensor.get_current_index() + 1]

    def get_read_deltas(self):
        return self.readDeltas[:self.amountReadsConducted]

    def get_read_times(self):
        return self.readTimes[:self.amountReadsConducted]

    def get_proposed_interval_diameters(self):
        return self.proposed_interval_diameter[:self.amountReadsConducted]

    def get_proposed_read_distances(self):
        return self.tdDeltas[:self.amountReadsConducted]

    # Compute statistics

    def get_percentage_error_larger_than(self, threshold):
        """
        :param threshold:  Threshold in sensor - read values
        :return:           The percentage of errors larger than #threshold
        """
        si = self.get_error()
        return np.sum(np.abs(si) > threshold) / si.shape[0]

    def get_error(self):
        return np.abs(self.get_available_data() - self.get_observed_data())

    def get_error_ratio(self):
        sd = self.get_available_data()
        if len(sd.shape) == 1:
            sd = sd[:, np.newaxis]
        arr = [np.mean(np.linalg.norm(sd[max(i - 1000, 0): i + 1000], axis=1)) for i in
               range(0, self.sensor.get_current_index() + 1)]
        arr = np.array([a if a > 0 else 1 for a in arr])
        diff = np.abs((self.get_available_data() - self.get_observed_data()))
        if len(diff.shape) > 1:
            diff = np.sum(diff, axis=1)
        return diff / arr
        # m = np.mean(np.abs(self.get_available_data()))
        # return np.abs((self.get_available_data() - self.get_observed_data()) / (m if m else 1))

    def get_error_mean(self):
        return np.mean(self.get_error_ratio())

    # def get_error_mean(self): return np.sum(self.get_error_ratio())
    def get_error_var(self):
        return np.var(self.get_error_ratio())

    def get_proposed_interval_diameter_mean(self):
        return np.mean(self.get_proposed_interval_diameters())

    def get_proposed_interval_diameter_var(self):
        return np.var(self.get_proposed_interval_diameters())

