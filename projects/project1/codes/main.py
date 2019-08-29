from os import system
import sys
N = int(sys.argv[1])

#Compile and execute program:
print("Compiling code...")
system("c++ -O3 -c project1.cpp")
system("c++ -O3 -o project1.exe project1.o")
print("Compilation finished, executing program...")


#run program for all n in number_of_gridpoints.
number_of_gridpoints = [int(10**((i))) for i in range(1,N+1)]
for n in number_of_gridpoints:
    print("Computing for n = " + str(n))
    system("./project1.exe" + " " + str(n) + " " + "solution_part_b_n_" + str(n) + ".txt")

print("Computations are done, making plots...")

#Create plots and move them to the folder ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb
for n in number_of_gridpoints:
    system("python3" + " " + "make_plot.py" +  " " + "solution_part_b_n_" + str(n) + ".txt")
    print("Plotting for n = " + str(n))

print("Plots are finished, Computing errors...")

#system("python3" + " " + "make_plot_subplots.py" + " " + "all_plots.png")

#print("subplots finished, computing maximum errors and writes it to a file...")

system("python3 compute_error.py" + " " + str(N))

print("Errors are computed, removing .txt files containing the computed solutions...")
#Remove txt-files to clear up space .
for n in number_of_gridpoints:
    system("rm" + " " + "solution_part_b_n_" + str(n) + ".txt")

print("Done")
