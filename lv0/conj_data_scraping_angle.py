'''
Bins the IMF cone and clock angles for every day in the range with available and reasonable data.
'''

from spacepy import pycdf
import bow_shock_model, csv
import numpy as np
from datetime import date, timedelta
from maths_tools import vector_angle


def bin_values(list, value):
    list[value][0] += 1
    return(list)

            ######### Initialise binned lists ########

clock_angle = [[0] for i in range(0, 360)]
cone_angle = [[0] for i in range(0, 360)]

conj_angles = []
crit_angle = 15
 
            ######### Get data ##########

data_loc = "S:/data/maven/maven/data/sci/kp/cdfs/"

#Open conjunction angle file
with open("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/conjunction-angles.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        #Add all numerical angles
        if len(row) != 0 and row[0] != "Year":   
            conj_angles.append(float(row[2]))

print("Opening CDFs")

for year in range(2022, 2023):
    for day in range(180, 540):
        #Check that Earth and Mars are aligned in the solar wind
        conj_index = 366*(year-1981) + day - 1
        if conj_angles[conj_index] <= crit_angle:
            day_num = str(day)
        
            #Day 1 of the year
            strt_date = date(year, 1, 1)

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
                    #Get CDF
                    cdf = pycdf.CDF(cdf_path)

                    #Extracts magnetic field components outside magnetosphere
                    print("    Extracting data for date " + res)
                    for i in range(0, len(cdf['SPICE_spacecraft_MSO'])):
                        #Get position vector
                        x = cdf['SPICE_spacecraft_MSO'][i][0]
                        y = cdf['SPICE_spacecraft_MSO'][i][1]
                        z = cdf['SPICE_spacecraft_MSO'][i][2]

                        b = cdf['MAG_field_MSO'][i]
                            
                        #Only accept reasonable (i.e. non-erroneous) data points
                        if b[0] > 10**3 or b[1] > 10**3 or b[2] > 10**3: 
                            continue
                        elif b[0] < -10**3 or b[1] < -10**3 or b[2] < -10**3:
                            continue
                        else:
                            #Append magnetic field data if MAVEN is in the solar wind AND Mars and Earth are within 0.25rad of conjunction in the IMF
                            if bow_shock_model.is_in_solarwind(x, y, z):
                                cone_angle = bin_values(cone_angle, round(vector_angle([1, 0, 0], b)))
                                clock_angle = bin_values(clock_angle, round(180/np.pi * np.atan2(b[1], b[2])))


                break

#Binned data location
loc = 'C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/MAVEN-data/solar-increasing/'

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