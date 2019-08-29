import numpy as np
import matplotlib.pyplot as plt
from os import system
import sys
N = int(sys.argv[1])

def error_function(v,u):
    if u != 0 and v!= 0:
        return np.log10(abs((v-u)/u))
    else:
        return 0

def u(x):
    """
    Analytical solution to the differential equation
    """
    return 1 - (1-np.exp(-10))*x - np.exp(-10*x)


#Gotta read data from many files simultanously and compute the error for each and write it to a file.
#This new file will be used to create a table.
max_error = []
number_of_gridpoints = [int(10**i) for i in range(1,N+1)]

H = [1/(float(i)+1) for i in number_of_gridpoints]
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
    h = 1/(float(n) + 1)

    x = np.array([(i+1)*h for i in range(n)])
    U = u(x)                    #Compute the corresponding values of u(x) at the same points as the data of v(x) is obtained.
    errors = np.zeros(n)        #Empty error array to store computed errors.
    for i in range(n):
        errors[i] = error_function(v[i], U[i])
        if abs(errors[i]) < 1e-1:
            errors[i] = -100

    max_error.append(np.max(errors[0:-1]))              #Finds the maximum error between v(x) and u(x).

with open("max_erromrs.txt", "w") as outfile:
    outfile.write("n" + " " + "max-error" + "\n")
    for i,e in zip(number_of_gridpoints, max_error):
        outfile.write(str("%.1E" % i) + " " + str("%f" % e) + "\n")

figurename = "max_error.png"
log_number_of_gridpoints = [np.log10(i) for i in number_of_gridpoints]
log_h = [np.log10(i) for i in H]
plt.plot(log_h, max_error)
plt.xlabel("log10(h)")
plt.ylabel("|log10(max error)|")
plt.title("Maximum error as a function number of gridpoints")
plt.savefig(figurename)
plt.close()

system("mv " + figurename + " ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb")
