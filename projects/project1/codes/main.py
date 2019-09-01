from os import system
import sys
N = int(sys.argv[1])

#Compile and execute program:
print("Compiling code...")
system("c++ -O3 -c project1.cpp functions.cpp")
system("c++ -O3 -o project1.exe project1.o functions.o")
#system("c++ -O3 -c project1_2.cpp")
#system("c++ -O3 -o project1_2.exe project1_2.o")
print("Compilation finished, executing program...")


#run program for all n in number_of_gridpoints.
number_of_gridpoints = [int(10**(i)) for i in range(1,N+1)]
for n in number_of_gridpoints:
    filename_solution = "solution_part_b_n_" + str(n) + ".txt"
    filename_errors = "errors_n_" + str(n) + ".txt"
    filename_time = "timeused_" + str(n) + ".txt"
    print("Computing for n = " + str(n))
    system("./project1.exe" + " " + str(n) + " " + filename_solution + " " + filename_errors + " " + filename_time)

print("Computations are done, making plots...")

#Create plots and move them to the folder ~/Documents/skole/comphys/projects/project1/codes/plots/plots_partb
for n in number_of_gridpoints:
    filename_solution = "solution_part_b_n_" + str(n) + ".txt"
    system("python3" + " " + "make_plot.py" +  " " + filename_solution)
    print("Plotting for n = " + str(n))

print("Plots are finished, creating a plot of the maximum relative error and writes the data to a file...")

system("python3" + " " + "find_max_error.py" + " " + str(N))

system("python3" + " " + "create_timetable.py" + " " + str(N))


print("Finished, removing unecessary .txt files...")
#Remove txt-files to clear up space .
for n in number_of_gridpoints:
    filename_solution = "solution_part_b_n_" + str(n) + ".txt"
    filename_errors = "errors_n_" + str(n) + ".txt"
    filename_time = "timeused_" + str(n) + ".txt"
    system("rm" + " " + filename_solution + " " + filename_errors + " " + filename_time)

print("Done")
