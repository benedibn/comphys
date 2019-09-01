from os import system
import sys
import numpy as np
import matplotlib.pyplot as plt

N = int(sys.argv[1])
number_of_gridpoints = [int(10**(i)) for i in range(1,N+1)]
max_error = []
for n in number_of_gridpoints:
    filename_errors = "errors_n_" + str(n) + ".txt"
    errors = []
    with open(filename_errors, "r") as infile:
        #timeused = float(infile.readline())   #Time used to run the c++ program.
        lines = infile.readlines()
        for line in lines:
            numbers = line.split()
            for number in numbers:
                errors.append(float(number))
    max_error.append(max(errors))


with open("max_errors.txt", "w") as outfile:
    outfile.write("n" + " " + "max-error" + "\n")
    for i,e in zip(number_of_gridpoints, max_error):
        outfile.write(str("%.1E" % i) + " " + str("%f" % e) + "\n")


h = [1/(float(i) + 1) for i in number_of_gridpoints]
log_h = [np.log10(i) for i in h]

figurename = "max_error.png"
plt.plot(log_h, max_error)
plt.xlabel("log10(h)")
plt.ylabel("log10(max error)")
plt.savefig(figurename)
system("mv " + figurename + " ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb")
plt.close()
