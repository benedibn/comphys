import numpy as np
import matplotlib.pyplot as plt
from os import system
import sys

#filename  = str(input("Type filename with extension: "))
filename = str(sys.argv[1])
v = []
with open(filename, "r") as infile:
    timeused = float(infile.readline())   #Time used to run the c++ program.
    lines = infile.readlines()
    for line in lines:
        numbers = line.split()
        for number in numbers:
            v.append(float(number))

v = np.array(v)

def u(x):
    """
    Analytical solution to the differential equation
    """
    return 1 - (1-np.exp(-10))*x - np.exp(-10*x)

n = len(v)
x = np.linspace(0,1,n)
X = np.linspace(0,1,1001)


plt.plot(x,v, label="Numerical solution with n = " + str(n))
plt.plot(X,u(X), label="Analytical solution")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.title("Simulation time = " + str(timeused) + " s")
plt.legend()

figurename = filename.strip(".txt") + ".png"
plt.savefig(figurename)
plt.show()
system("mv " + figurename + " ~/Documents/skole/comphys/projects/project1/codes/plots")
