from os import system
import sys

number_of_gridpoints = [10, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7]
number_of_gridpoints = [int(i) for i in number_of_gridpoints]

#run program for all n in number_of_gridpoints.
for n in number_of_gridpoints:
    system("./project1_partb.exe" + " " + str(n) + " " + "solution_part_b_n_" + str(n) + ".txt")

print("Computations are done, making plots...")

#Create plots and move them to the folder ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb
for n in number_of_gridpoints:
    system("python3" + " " + "make_plot.py" +  " " + "solution_part_b_n_" + str(n) + ".txt")

print("Plots are finished, making congregation of plots...")

system("python3" + " " + "make_plot_subplots.py" + " " + "all_plots.png")

print("congregation of plots are finished, removing .txt files...")
#Remove txt-files to clear up space .
for n in number_of_gridpoints:
    system("rm" + " " + "solution_part_b_n_" + str(n) + ".txt")

print("Done")
