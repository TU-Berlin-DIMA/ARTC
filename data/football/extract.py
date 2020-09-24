import numpy as np
import matplotlib.pyplot as plt
import sys

plot  = len(sys.argv) > 1 and int(sys.argv[1]) & 2

i = np.loadtxt("+debs2013.data", delimiter=',').astype("double")
i = i[i[:,1].argsort()]   # sort by time if that is not yet the case
out4 = i[(i[:, 0]  == 4)] 
np.savetxt("data.csv", out4[:3600000,9], delimiter=',')

if plot:
    plt.figure(figsize=(20,20))
    plt.plot(out4[:,7], color="blue")
    plt.plot(out4[:,8], color="red")
    plt.plot(out4[:,9], color="black")
    plt.show()
    plt.savefig("football.png")
