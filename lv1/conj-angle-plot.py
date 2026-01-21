import matplotlib.pyplot as plt
import csv

days = []
angles = []

#Read in clock angle
with open("c:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/conjunction-angles.csv", 'r') as csvfile:
    csvreader = csv.reader(csvfile) 

    fields = next(csvreader)
    for row in csvreader:  
        if len(row) != 0 and row[0] != "Year":
            if int(row[0])%4 ==0:
                #Leap year
                days.append((int(row[0])-1981)*366 + int(row[1]))
                angles.append(float(row[2]))
            else:
                #Normal year
                days.append((int(row[0])-1981)*365 + int(row[1]))
                angles.append(float(row[2]))

days.append(days[-1]+1)

fig, ax = plt.subplots(1,1)

#Plot magnitudes
ax.stairs(angles, days, color = 'xkcd:black')
plt.show()