'''
Plots:
    A histogram of the magnetic field strength between 0 and 20 nT
    A 2D histogram of the magnetic field in the x-y plane
'''

import matplotlib.pyplot as plt 
import csv, maths_tools
import numpy as np


#Initialise arrays
matrix = []

#Binned data location
loc = 'C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/MAVEN-data/solar-declining/'

#Read in x-y matrix
with open(loc+"binned_xy.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 
    for row in csvreader:  
        if len(row) != 0:
            row_ints = [int(x) for x in row]   
            matrix.append(row_ints)



        ######### bx/by preprocessing ########

#Reverse the list so that B_y decreases along the vertical axis
matrix = matrix[::-1]

        ######## Plotting ########

#Initialise figure
fig, ax1 = plt.subplots(1, 1)

fig.suptitle("Magnetic field distribution")


#Plot x-y data
h = ax1.imshow(matrix, cmap = 'binary', extent = [-20, 20, -20, 20])
ax1.set_xlabel("$B_x$ (nT)")
ax1.set_ylabel("$B_y$ (nT)")
ax1.set_xlim([-10, 10])
ax1.set_ylim([-10, 10])
ax1.minorticks_on()


#Colorbar
fig.colorbar(h, ax=ax1, label = 'Frequency')

plt.show()