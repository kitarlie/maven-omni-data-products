'''
Bins the IMF cone and clock angles for every day in the range with available and reasonable data.

Switch between every day with data and only days with Mars-Earth conjunctions in the IMF using line 78
'''

import csv
import numpy as np
from maths_tools import vector_angle


def bin_values(list, value):
    list[value][0] += 1
    return(list)

            ######### Initialise binned lists ########

clock_angle = [[0] for i in range(0, 360)]
cone_angle = [[0] for i in range(0, 360)]
 
            ######### Get data ##########

data_loc = "S:/data/omni/omni_1min_monthly/"

for year in range(1981, 2024):
    for month in range(1, 13):
        month_txt = str(month)
        if len(month_txt) == 1:
            month_txt = "0" + month_txt
        try:
            ascii_grid = np.loadtxt(data_loc + "omni_min" + str(year) + month_txt + ".asc")
        except FileNotFoundError:
            print("No file located for " + month_txt + "-" + str(year))
            continue
        else:
            print("File located for " + month_txt + "-" + str(year))
            for row in ascii_grid:
                    b = [float(row[14]), float(row[15]), float(row[16])]
                    if abs(b[0]) > 999 or abs(b[1]) > 999 or abs(b[2]) > 999:
                        continue
                    else:
                        cone_angle = bin_values(cone_angle, round(vector_angle([1, 0, 0], b)))
                        clock_angle = bin_values(clock_angle, round(180/np.pi * np.atan2(b[1], b[2])))

#Binned data location
loc = 'C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/OMNI-data/all-time/binned/'

print("Writing data")

#Write the x-component data to a CSV
with open(loc+"binned_clock-angle.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(clock_angle) 

#Write the cone angle to a CSV
with open(loc+"binned_cone-angle.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(cone_angle) 

print("Data stored!")