'''
Runs over MAVEN CDF files and bins the magnetic field components + magnitude in frequency tables

Switch between every day with data and only days with Mars-Earth conjunctions in the IMF using line 95
'''

import numpy as np, csv
from spacepy import pycdf
from bow_shock_model import is_in_solarwind
from datetime import date, timedelta
from mars_earth_alignment import get_mars_time

conj_angles = []
crit_angle = 15

#Open conjunction angle file
with open("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/conjunction-angles.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        #Add all numerical angles
        if len(row) != 0 and row[0] != "Year":   
            conj_angles.append(float(row[2]))

data_loc = "S:/data/omni/omni_1min_monthly/"
mvn_loc = "S:/data/maven/maven/data/sci/kp/cdfs/"

def bin_data(binned, value):
    #Index based on value
    i = int(value*10)
    try:
        #Increment frequency
        current = binned[i]
    except IndexError:
        return binned
    else:
        binned[i][1] += 1
        return binned

#Initialise lists
bs = [[x/10, 0] for x in range(0, 10000)]

for year in range(2022, 2023):
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
                conj_index = 366*(year-1981) + int(row[1]) - 1
                if conj_angles[conj_index] <= crit_angle:
                    #[year, day, hour, min, second]
                        mvn_time = get_mars_time([row[0], row[1], row[2], row[3]], row[21])

                        #Day 1 of the year
                        strt_date = date(int(mvn_time[0]), 1, 1)

                        #Convert to date
                        res_date = strt_date + timedelta(days=int(mvn_time[1]) - 1)
                        res = res_date.strftime("%Y%m%d")

                        for i in range(20, -1, -1):
                            if i == 0:
                                continue
                            cdf_path = mvn_loc + "mvn_insitu_kp-4sec_" + res + "_v" + str(i)+ "_r01.cdf"
                            try:
                                cdf = pycdf.CDF(cdf_path)
                            except pycdf.CDFError:
                                continue
                            else:
                                cdf = pycdf.CDF(cdf_path)
                                i = int((mvn_time[2]*60*60 + mvn_time[3]*60 + mvn_time[4])/(24*60*60))

                                x = cdf['SPICE_spacecraft_MSO'][i][0]
                                y = cdf['SPICE_spacecraft_MSO'][i][1]
                                z = cdf['SPICE_spacecraft_MSO'][i][2]

                                if is_in_solarwind(x, y, z):
                                    #GSE/GSM b_x
                                    bx = float(row[14])
                                    #GSE b_y
                                    by = float(row[15])
                                    #GSE b_z
                                    bz = float(row[16])
                                    #Magnitude
                                    b = np.sqrt(bx**2 + by**2 + bz**2)

                                    bs = bin_data(bs, round(b, 1))

#Binned data location
loc = 'C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/OMNI-data/solar-increasing/'

#Write the magnitude data to a CSV
with open(loc+"binned_mag.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["b", "frequency"])
    csvwriter.writerows(bs) 

print("Data scraped!")