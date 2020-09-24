class PID:

    def __init__(self, set_point=0.0, param_p=0.6, param_i=0.1, param_d=0.4, min_time_diff=1, forgetfulness=.8):
        assert(min_time_diff > 0)

        # save parameters 
        self.set_point = set_point
        self.Kp = param_p
        self.Ki = param_i
        self.Kd = param_d
        self.min_time_diff = min_time_diff
        self.forgetfulness = forgetfulness
        
        # set internal variables
        self.lastTime = -1
        self.lastError = 0
        self.output = 0.0
        self.iTerm = 0.0

    def next(self, t, feedback):
        assert(t >= 0 and t > self.lastTime)
        error = self.set_point - feedback
        delta_time = t - self.lastTime
        delta_error = error - self.lastError

        if delta_time >= self.min_time_diff:
            assert(delta_time > 0)
            
            # Compute output
            if self.lastTime >= 0:
                if self.forgetfulness == 1:
                    self.iTerm = (self.iTerm + error * delta_time) / t
                self.iTerm = self.iTerm * self.forgetfulness + error * delta_time
                self.output = error + (self.Ki * self.iTerm) + (self.Kd * delta_error / delta_time)
            
            # Update last t and value
            self.lastTime = t
            assert(self.lastTime >= 0)
        else:
            print(delta_time, "error")
        self.lastError = error

        return self.output

