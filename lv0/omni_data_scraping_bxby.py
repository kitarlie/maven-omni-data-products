'''
Runs over MAVEN CDF files and bins the x- and y-components in a 2D frequency table

Switch between every day with data and only days with Mars-Earth conjunctions in the IMF using line 80
'''

import csv, maths_tools
import numpy as np


def binning(data_matrix, bx, by):
    #Check whether values are within the range allowed by the matrix.
    if bx < -20 or bx >= 20:
        #print("B_x out of bounds")
        return data_matrix
    elif by < -20 or by >= 20:
        #print("B_y out of bounds")
        return data_matrix
    else:
        i = int(2*by) + 40
        j = int(2*bx) + 40
        data_matrix[i][j] += 1
        return data_matrix


#80x80 data matrix, containg values for B in the interval -20 nT <= B < 20 nT with resolution 0.5 nT
data_matrix = [[0]*80 for i in range(0, 80)]

            ######### Get data ##########

data_loc = "S:/data/omni/omni_1min_monthly/"

print("Opening files")

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
                #GSE/GSM b_x
                bx = float(row[14])
                #GSE b_y
                by = float(row[15])
                #Update magnetic field frequency if MAVEN is in the solar wind
                data_matrix = binning(data_matrix, maths_tools.round_half_int(float(bx)), maths_tools.round_half_int(float(by)))


            ######## Write data to CSV ########

#Binned data location
loc = 'C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/OMNI-data/all-time/binned/'


#Write the data matrix data to a CSV
print("Writing data")
with open(loc+"binned_xy.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(data_matrix) 

print("Data stored!")