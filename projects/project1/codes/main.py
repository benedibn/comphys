from os import system
import sys

#Compile and execute program:
system("c++ -c -O3 -Wall project1.cpp")
system("c++ -o project1.exe project1.o")
print("Compilation finished, executing program...")


number_of_gridpoints = [10, 50, 1e2, 5e2, 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6, 1e7]
number_of_gridpoints = [int(i) for i in number_of_gridpoints]

#run program for all n in number_of_gridpoints.
for n in number_of_gridpoints:
    print("Computing for n = " + str(n))
    system("./project1.exe" + " " + str(n) + " " + "solution_part_b_n_" + str(n) + ".txt")

print("Computations are done, making plots...")

#Create plots and move them to the folder ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb
for n in number_of_gridpoints:
    system("python3" + " " + "make_plot.py" +  " " + "solution_part_b_n_" + str(n) + ".txt")
    print("Plotting for n = " + str(n))

print("Plots are finished, creating subplots...")

system("python3" + " " + "make_plot_subplots.py" + " " + "all_plots.png")

print("subplots finished, computing maximum errors and writes it to a file...")

system("python3 compute_error.py")

print("Errors are computed, removing .txt files containing the computed solution...")
#Remove txt-files to clear up space .
for n in number_of_gridpoints:
    system("rm" + " " + "solution_part_b_n_" + str(n) + ".txt")

print("Done")
