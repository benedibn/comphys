import numpy as np
import matplotlib.pyplot as plt

filename  = str(input("Type filename with extension: "))
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
x = np.linspace(0,1,n)

plt.plot(x,v, label="Numerical solution")
plt.plot(x,u(x), label="Analytical solution")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.legend()
plt.savefig("solution_n_" + str(n) + ".png")
plt.show()
