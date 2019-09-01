from os import system
import sys

N = int(sys.argv[1])
number_of_gridpoints = [int(10**(i)) for i in range(1,N+1)]

time_used = []
for n in number_of_gridpoints:
    filename_time = "timeused_" + str(n) + ".txt"
    with open(filename_time, "r") as infile:
        time = float(infile.readline())
        time_used.append(time)


filename = "n_vs_time.txt"
with open(filename, "w") as outfile:
    outfile.write("n" + " " + "time/s" + "\n")
    for n, time in zip(number_of_gridpoints, time_used):
        outfile.write(str("%.1E" % n) + " " + str("%f" % time) + "\n")
