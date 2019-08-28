import numpy as np
import matplotlib.pyplot as plt
from os import system


def error_function(v,u):
    if u != 0 and v!= 0:
        return np.log10(abs((v-u)/u))
    else:
        return 0

def f(x):
    return 1-(1-np.exp(-10))*x - np.exp(-10*x)
zeta = -(-np.log(1-np.exp(-10))-np.log(10))/10
M1 = f(zeta)
M2 = 10**4


def u(x):
    """
    Analytical solution to the differential equation
    """
    return 1 - (1-np.exp(-10))*x - np.exp(-10*x)

def estimated_max_error(h):
    eps = (h**2/12)*M1 + ((4e-15)/h**2)*M2
    return np.log10(eps)

#Gotta read data from many files simultanously and compute the error for each and write it to a file.
#This new file will be used to create a table.
max_error = []
number_of_gridpoints = [10, 50, 1e2, 5e2, 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6, 1e7]
number_of_gridpoints = [int(i) for i in number_of_gridpoints]
h = [1/(float(i)+1) for i in number_of_gridpoints]
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
    x = np.linspace(0, 1, n+1)
    U = u(x)                    #Compute the corresponding values of u(x) at the same points as the data of v(x) is obtained.
    errors = np.zeros(n)        #Empty error array to store computed errors.
    for i in range(n-1):
        errors[i] = error_function(v[i], U[i+1])
        if abs(errors[i]) < 1e-2:
            errors[i] = 0
        #print(errors[i])
        errors[-1] = 0

    max_error.append(np.mean(errors))              #Finds the maximum error between v(x) and u(x).

max_error_estimation = list(map(f,h))
with open("max_errors.txt", "w") as outfile:
    outfile.write("n" + " " + "max-error" + "\n")
    for i,e in zip(number_of_gridpoints, max_error):
        outfile.write(str("%.1E" % i) + " " + str("%f" % e) + "\n")

figurename = "max_error.png"
log_number_of_gridpoints = [np.log10(i) for i in number_of_gridpoints]
log_h = [np.log10(i) for i in h]
plt.plot(log_h, max_error)
plt.xlabel("log10(h)")
plt.ylabel("|log10(max error)|")
plt.title("Maximum error as a function number of gridpoints")
plt.savefig(figurename)
plt.close()

system("mv " + figurename + " ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb")
