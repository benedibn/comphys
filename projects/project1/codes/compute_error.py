import numpy as np
import matplotlib.pyplot as plt


#Gotta read data from many files simultanously and compute the error for each and write it to a file.
#This new file will be used to create a table.

def error_function(v,u):
    return np.log10(abs((v-u)/u))

U = u(x)                    #Compute the corresponding values of u(x) at the same points as the data of v(x) is obtained.
errors = np.zeros(n)        #Empty error array to store computed errors.
for i in range(n):
    errors[i] = error_function(v[i], U[i])

max_error = max(errors)     #Finds the maximum error between v(x) and u(x).
