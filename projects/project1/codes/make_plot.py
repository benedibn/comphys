import numpy as np
import matplotlib.pyplot as plt
from os import system
import sys

#filename  = str(input("Type filename with extension: "))
filename = str(sys.argv[1])
v = []
with open(filename, "r") as infile:
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
h = 1/(float(n) + 1)
x = [float((i+1)*h) for i in range(n)]
x = np.array(x)
#x = np.linspace(0,1,n+1)
#x = [(i+1)*h for i in range(n)]
#x = np.array(x)
#X = np.linspace(0,1,1001)
print(x[0:2])

plt.plot(x,v, label="Numerical solution with n = " + str(n))
plt.plot(x,u(x), label="Analytical solution")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.legend()

figurename = filename.strip(".txt") + ".png"
plt.savefig(figurename)
system("mv " + figurename + " ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb")
plt.close()
