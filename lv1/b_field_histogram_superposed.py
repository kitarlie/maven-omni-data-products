'''
Plots:
    A histogram of the magnetic field strength between 0 and 20 nT
'''

import matplotlib.pyplot as plt 
import csv, maths_tools
import numpy as np


#Initialise arrays
b = []
b_omni = []

#Binned data location
mvn_loc = 'C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/MAVEN-data/cmes/2018-186/'
omni_loc = 'C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/OMNI-data/cmes/2018-186/'

#Read in magnitudes
with open(mvn_loc+"binned_mag.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        if len(row) != 0:   
            b.append(row)

with open(omni_loc+"binned_mag.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        if len(row) != 0:   
            b_omni.append(row)


        ######### MAVEN preprocessing ########

#Split into two separate lists
bs = [maths_tools.round_half_int(float(b[i][0])) for i in range(len(b))]
freq = [int(b[i][1]) for i in range(len(b))]

bs_half_int = []
freq_half_int = []

#Re-bin data to half-integer values
for b in bs:
    i = bs.index(b)
    if b in bs_half_int:
        j = bs_half_int.index(b)
        freq_half_int[j] += freq[i]
    else:
        bs_half_int.append(b)
        freq_half_int.append(freq[i])

#Normalise data
total_counts = np.sum(freq_half_int)
freq_half_int_norm = [f/total_counts for f in freq_half_int]

#Add extra row as endpoint for step plot
bs_half_int.append(bs_half_int[-1]+0.5)

        ######### OMNI preprocessing ########

#Split into two separate lists
bs_omni = [maths_tools.round_half_int(float(b_omni[i][0])) for i in range(len(b_omni))]
freq_omni = [int(b_omni[i][1]) for i in range(len(b_omni))]

bs_half_int_omni = []
freq_half_int_omni = []

#Re-bin data to half-integer values
for b_omni in bs_omni:
    i = bs_omni.index(b_omni)
    if b_omni in bs_half_int_omni:
        j = bs_half_int_omni.index(b_omni)
        freq_half_int_omni[j] += freq_omni[i]
    else:
        bs_half_int_omni.append(b_omni)
        freq_half_int_omni.append(freq_omni[i])

#Normalise data
total_counts = np.sum(freq_half_int_omni)
freq_half_int_omni_norm = [f/total_counts for f in freq_half_int_omni]

#Add extra row as endpoint for step plot
bs_half_int_omni.append(bs_half_int[-1]+0.5)

        ######## Plotting ########

#Initialise figure
fig, ax1 = plt.subplots(1, 1)

fig.suptitle("Magnetic field distribution")

            ######## Histogram of magnitude ########

#Plot magnitudes
ax1.stairs(freq_half_int_norm, bs_half_int, color = 'xkcd:red')
ax1.stairs(freq_half_int_omni_norm, bs_half_int_omni, color = 'xkcd:blue')

#Title
ax1.set_xlabel("$|B|$ (nT)")
ax1.set_ylabel("% occurrence")
ax1.minorticks_on()
ax1.set_xlim([0, 20])


plt.show()