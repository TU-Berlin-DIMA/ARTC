from globalParams import max_amount_samples

import numpy as np


class Sensor:
    """ 
    Representation of a physical sensor, which only delivers data. 
    """
    
    def __init__(self, name, data=np.array([])):
        """ 
        @param data: The scalar values of the currently replayed dataset.
        """
        if not data.shape[0]:
            data = np.loadtxt(name, delimiter=",")[:max_amount_samples]
        assert(data.shape[0] > 0)

        # Values for looking up the next read:
        self.data = data                      # Data, available at highest possible frequency.
        self.currIndex = -1                   # Index of the last read in the #data
        self.currValue = float('nan')         # Last value read from sensor.
        self.name = name

    # Read and access last read:

    def read(self, index_delta):
        """ 
        Read next value from sensor, store and return it and adapt the current time.
        @param index_delta:    amount of time (= samples) to skip in the array
        """
        assert(not self.is_almost_finished(index_delta))
        assert(index_delta > 0)

        # Conduct the sensor read
        self.currIndex += index_delta
        self.currValue = self.data[self.currIndex]

    def get_current_value(self):
        """ Return the value acquired through the last sensor read. """
        assert(self.is_started())
        return self.currValue
    
    def get_current_index(self):
        """ Return the value acquired through the last sensor read. """
        assert(self.is_started())
        return self.currIndex

    # Query the state of the sensor:

    def is_started(self):
        """ Returns whether at least one value has already been read from the sensor. """
        return self.currIndex >= 0

    def is_almost_finished(self, index_delta):
        """
        Returns whether the sensor is out of data when requesting a sample in #index_delta
        time units.
        """
        return self.currIndex + index_delta >= self.data.shape[0]

