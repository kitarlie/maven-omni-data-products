import numpy as np, requests, json, csv
from datetime import datetime, date, timedelta
from mars_earth_alignment import get_mars_time
from bow_shock_model import is_in_solarwind
from spacepy import pycdf

conj_angles = []
omni_loc = "S:/data/omni/omni_1min_monthly/"
mvn_loc = "S:/data/maven/maven/data/sci/kp/cdfs/"

#Contains Earth and Mars arrival times []
results = []

#Open conjunction angle file
with open("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/conjunction-angles.csv", 'r') as csvfile:
    print("Reading in conjunction angles")
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        #Add all numerical angles
        if len(row) != 0 and row[0] != "Year":   
            conj_angles.append(float(row[2]))

#Call the CCMC CME scoreboard API and convert the JSON object to a dictionary
print("Getting CME database")
x = json.loads(requests.get('https://kauai.ccmc.gsfc.nasa.gov/CMEscoreboard/WS/get/predictions').text)

for cme in x:
    #Check that the CME arrived at Earth
    if cme['noArrivalObserved'] == False:
        year = int(cme['observedTime'][0:4])
        #Check that data is in range of conj_angles (currently goes up to end of 2025)
        if year < 2026:
            #Get day as a datetime object
            dt = datetime(year, int(cme['observedTime'][5:7]), int(cme['observedTime'][8:10]))
            #Convert to day of year
            doy = dt.timetuple().tm_yday
            #Get corresponding index in conj_angles
            conj_index = 366*(year-1981) + int(doy) - 1

            print("Checking CME detected at " + cme['observedTime'])
            if conj_angles[conj_index] <= 15:
                print("    Earth and Mars aligned")
                try:
                    ascii_grid = np.loadtxt(omni_loc + "omni_min" + str(year) + cme['observedTime'][5:7] + ".asc")
                except FileNotFoundError:
                    print("No file located for " + cme['observedTime'][5:7] + "-" + str(year))
                    continue
                for row in ascii_grid:
                    if int(row[1]) == doy and int(row[2]) == int(cme['observedTime'][11:13]) and int(row[3]) == int(cme['observedTime'][14:16]):
                        print("    OMNI data matched")
                        #[year, day, hour, min, second]
                        mvn_time = get_mars_time([row[0], row[1], row[2], row[3]], row[21])

                        #Flags whether there is MAVEN data near the CME arrival: True if there is any period where MAVEN is in the solar wind
                        good_result = False

                        #Day 1 of the year
                        strt_date = date(int(mvn_time[0]), 1, 1)

                        #Convert arrival day to date
                        res_date = strt_date + timedelta(days=int(mvn_time[1]) - 1)
                        res = res_date.strftime("%Y%m%d")

                        #Open CDF for arrival dat
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
                                #Check whether MAVEN leaves the magnetosphere on the arrival
                                for entry in cdf['SPICE_spacecraft_MSO']:
                                    if is_in_solarwind(entry[0], entry[1], entry[2]):
                                        good_result = True

                        #Convert arrival day to date
                        res_date = strt_date + timedelta(days=int(mvn_time[1]))
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
                                for entry in cdf['SPICE_spacecraft_MSO']:
                                    if is_in_solarwind(entry[0], entry[1], entry[2]):
                                        good_result = True

                        if good_result:
                            print("    MAVEN data matched")
                            results.append([int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(mvn_time[0]), int(mvn_time[1]), int(mvn_time[2]), int(mvn_time[3])])
                        break

with open("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/cme-arrivals.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Year (Earth)", "Day (Earth)", "Hour (Earth)", "Minute (Earth)", "Year (Mars)", "Day (Mars)", "Hour (Mars)", "Minute (Mars)"])
    for result in results:
        csvwriter.writerow(result)