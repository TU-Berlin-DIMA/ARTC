
import numpy as np
import matplotlib.pyplot as plt

import sys

path1 = "data/"
activities = [1, 2, 6, 7, 13]
persons = range(1, 9)

small = len(sys.argv) > 1 and int(sys.argv[1]) & 1
plot  = len(sys.argv) > 1 and int(sys.argv[1]) & 2
sessions = 5 if small else 60
output_file = "small.csv" if small else "data.csv"

data = np.array(0)
data2 = np.array(0)

for person in persons:

    for activity in activities:
        act = ("0" if activity < 10 else "") + str(activity)
        path2 = path1 + "a" + act + "/p" + str(person) + "/s"

        for i in range(sessions):
            k = (i+1)
            k = ("0" + str(k)) if k < 10 else str(k)


            l = np.loadtxt(path2 + k + ".txt", delimiter=",")
            data = np.vstack((data, l))  if len(data.shape) else l
            il = np.ones([l.shape[0]])* activity
            data2 = np.hstack((data2, il)) if len(data2.shape) else il

np.savetxt(output_file, data[:,0], delimiter=",")

if plot:
    plt.figure(figsize=(10, 10))
    for i in range(9):
        plt.subplot(3, 3, i+1)
        plt.plot(data[ :, 9*0+ i ])
        plt.plot(data2)
    plt.show()

