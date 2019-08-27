import numpy as np
import matplotlib.pyplot as plt
from os import system


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
number_of_gridpoints = [10, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7]
number_of_gridpoints = [int(i) for i in number_of_gridpoints]
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
    x = np.linspace(0,1, n)
    U = u(x)                    #Compute the corresponding values of u(x) at the same points as the data of v(x) is obtained.
    errors = np.zeros(n)        #Empty error array to store computed errors.
    for i in range(n):
        errors[i] = error_function(v[i], U[i])

    max_error.append(max(errors))     #Finds the maximum error between v(x) and u(x).

print(max_error)
with open("max_errors.txt", "w") as outfile:
    outfile.write("n" + " " + "max_error" + "\n")
    for i,e in zip(number_of_gridpoints, max_error):
        outfile.write(str(i) + " " + str(e) + "\n")

figurename = "max_error.png"
log_number_of_gridpoints = [np.log10(i) for i in number_of_gridpoints]
plt.plot(log_number_of_gridpoints, max_error)
plt.xlabel("log10(n)")
plt.ylabel("log10(max error)")
plt.title("Maximum error as a function number of gridpoints")
plt.savefig(figurename)
plt.close()

system("mv " + figurename + " ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb")
