from spacepy import pycdf
import bow_shock_model
import numpy as np
import csv
import os
from dotenv import load_dotenv
from datetime import date, timedelta

#Load in environment variables
load_dotenv("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Code/data_locations.env")

def binning(data_matrix, bx, by):
    #Check whether values are within the range allowed by the matrix.
    if bx < -20 or bx >= 20:
        print("B_x out of bounds")
        return data_matrix
    elif by < -20 or by >= 20:
        print("B_y out of bounds")
        return data_matrix
    else:
        i = by + 20
        j = bx + 20
        data_matrix[i][j] += 1
        return data_matrix



data_matrix = [[0]*40 for i in range(0, 40)]

            ######### Get data ##########

data_loc = os.getenv("DATA_LOC")

print("Opening CDFs")

for year in range(2014, 2025):
    #Ensure loop is killed when all data is binned
    if year == 2024:
        break
    for day in range(0, 366):
        day_num = str(day)
        year = str(year)
    
        #Day 1 of the year
        strt_date = date(int(year), 1, 1)

        #Convert to date
        res_date = strt_date + timedelta(days=int(day_num) - 1)
        res = res_date.strftime("%Y%m%d")
        
        #Iterate over any possible version number
        for i in range(20, -1, -1):
            if i == 0:
                print("No data file located for date " + res)
                continue
            cdf_path = data_loc + "mvn_insitu_kp-4sec_" + res + "_v" + str(i)+ "_r01.cdf"
            try:
                cdf = pycdf.CDF(cdf_path)
            except pycdf.CDFError:
                continue
            else:
                print("File located for date " + res)
                #Get CDF path
                cdf = pycdf.CDF(cdf_path)

                #Extracts magnetic field components outside magnetosphere
                print("    Extracting data for date " + res)
                for i in range(0, len(cdf['SPICE_spacecraft_MSO'])):
                    #Get position vector
                    x = cdf['SPICE_spacecraft_MSO'][i][0]
                    y = cdf['SPICE_spacecraft_MSO'][i][1]
                    z = cdf['SPICE_spacecraft_MSO'][i][2]

                    if i == 0:
                        print("    Binning data")

                    #Update magnetic field frequency if MAVEN is in the solar wind
                    if bow_shock_model.is_in_solarwind(x, y, z):
                        data_matrix = binning(data_matrix, int(cdf['MAG_field_MSO'][i][0]), int(cdf['MAG_field_MSO'][i][1]))

                break


            ######## Write data to CSV ########

#Binned data location
loc = os.getenv("STORAGE_LOC")

sum = 0
for i in data_matrix:
    for j in i:
        sum += j


#Write the data matrix data to a CSV
print("Writing data")
with open(loc+"binned_xy.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(data_matrix) 

print("Data stored!")