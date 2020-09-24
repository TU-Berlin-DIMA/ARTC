import numpy as np
import matplotlib.pyplot as plt
import sys

plot  = len(sys.argv) > 1 and int(sys.argv[1]) & 2

out = np.loadtxt("ethylene_CO.txt", dtype=str, skiprows=1)
out = out[out[:,0].astype("double").argsort()]   # sort by time if that is not yet the case
out = out[:360000,11].astype("double")
np.savetxt("data.csv", out, delimiter=',')

if plot:
    plt.figure(figsize=(20,20))
    plt.plot(out, color="black")
    plt.show()
    plt.savefig("gas.png")
