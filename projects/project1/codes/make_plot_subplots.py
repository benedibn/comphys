import numpy as np
import matplotlib.pyplot as plt
from os import system
import sys

def u(x):
    """
    Analytical solution to the differential equation
    """
    return 1 - (1-np.exp(-10))*x - np.exp(-10*x)


#filename  = str(input("Type filename with extension: "))
number_of_gridpoints = [10, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7]
number_of_gridpoints = [int(i) for i in number_of_gridpoints]
figurename = str(sys.argv[1])
i = 0
for n in number_of_gridpoints:
    filename = "solution_part_b_n_" + str(n) + ".txt"
    v = []
    with open(filename, "r") as infile:
        timeused = float(infile.readline())   #Time used to run the c++ program.
        lines = infile.readlines()
        for line in lines:
            numbers = line.split()
            for number in numbers:
                v.append(float(number))

    v = np.array(v)

    x = np.linspace(0,1,n)
    X = np.linspace(0,1,1001)

    plt.subplot(420 + i + 1)
    plt.plot(x,v, label="n = " + str(n))
    plt.plot(X,u(X))
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.legend()
    i += 1

plt.savefig(figurename)
system("mv " + figurename + " ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb")
plt.close()
