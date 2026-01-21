'''
Runs over MAVEN CDF files and bins the magnetic field components + magnitude in frequency tables

Switch between every day with data and only days with Mars-Earth conjunctions in the IMF using line 95
'''

from spacepy import pycdf
import bow_shock_model, csv
import numpy as np
from datetime import date, timedelta


def bin_data(binned, value):
    #Index based on value
    i = int(value*10)
    try:
        #Check that value is within allowed range
        current = binned[i]
    except IndexError:
        return binned
    else:
        #Increment frequency
        binned[i][1] += 1
        return binned

#Initialise lists
bs = [[x/10, 0] for x in range(0, 10000)]
 
            ######### Get data ##########

data_loc = "S:/data/maven/maven/data/sci/kp/cdfs/"

print("Opening CDFs")

for year in range(2014, 2025):
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
                for i in range(0, len(cdf['SPICE_spacecraft_MSO'])):
                    #Get position vector
                    x = cdf['SPICE_spacecraft_MSO'][i][0]
                    y = cdf['SPICE_spacecraft_MSO'][i][1]
                    z = cdf['SPICE_spacecraft_MSO'][i][2]

                    b = cdf['MAG_field_MSO'][i]

                    #Only accept reasonable (i.e. non-erroneous) data points
                    if abs(b[0]) >= 10**3 or abs(b[1]) >= 10**3 or abs(b[2]) >= 10**3: 
                        continue
                    else:
                        if i == 0:
                            print("    Extracting data for date " + res)
                        #Append magnetic field data if MAVEN is in the solar wind
                        if bow_shock_model.is_in_solarwind(x, y, z):
                            bs = bin_data(bs, np.linalg.norm(b))
                break


if bs[-1][0] == np.inf:
    bs.pop(-1)

#Binned data location
loc = 'C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/MAVEN-data/all-time/binned/'

#Write the magnitude data to a CSV
with open(loc+"binned_mag.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["b", "frequency"])
    csvwriter.writerows(bs) 

print("Data scraped!")