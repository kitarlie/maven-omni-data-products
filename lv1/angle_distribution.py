'''
Plots histograms of the binned clock and cone angles
'''

import matplotlib.pyplot as plt 
import csv


#Initialise arrays
clock_angle = []
cone_angle = []

clockangles = range(-180, 181)
coneangles = range(0, 181)

#Binned data location
loc = "C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/MAVEN-data/solar-declining/"

#Read in clock angle
with open(loc+"binned_clock-angle.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        if len(row) != 0:   
            clock_angle.append(int(row[0]))

#Read in cone angle
with open(loc+"binned_cone-angle.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        if len(row) != 0:   
            cone_angle.append(int(row[0]))


        ######### Clock angle preprocessing ########

clock_angle_neg_quart = clock_angle[180::]
for i in range(0, 180):
    clock_angle_neg_quart.append(clock_angle[i])
clock_angle = clock_angle_neg_quart
clock_angle.append(clock_angle[0])


        ######### Cone angle preprocessing ########

cone_angle = cone_angle[:180:]


        ######## Plotting ########

#Initialise figure
fig, (ax1, ax2) = plt.subplots(2, 1)

fig.suptitle("Angle distribution")

            ######## Histogram of clock angle ########

#Plot clock angles
ax1.stairs(clock_angle, clockangles, color = 'xkcd:black')

#Formatting
ax1.set_xlabel("IMF clock angle (degrees)")
ax1.set_ylabel("Frequency")
ax1.set_xlim([-180, 180])
ax1.set_xticks([-180, -135, -90, -45, 0, 45,  90, 135, 180])

#Plot clock angles
ax2.stairs(cone_angle, coneangles, color = 'xkcd:black')

#Formatting
ax2.set_xlabel("IMF cone angle (degrees)")
ax2.set_ylabel("Frequency")
ax2.set_xlim([0, 180])
ax2.set_xticks([0, 45,  90, 135, 180])

plt.show()