from spacepy import pycdf
import matplotlib.pyplot as plt
import numpy as np
import bow_shock_model
import data_scraping
from data_scraping import bx, by, bz, b

bxs = []
bys = []
bzs = []
bs = []

print("Unpacking data")
for i in range(len(bx)):
    for j in range(bx[i][1]):
        bxs.append(bx[i][0])

for i in range(len(by)):
    for j in range(by[i][1]):
        bys.append(by[i][0])

for i in range(len(bz)):
    for j in range(bz[i][1]):
        bzs.append(bz[i][0])

for i in range(len(b)):
    for j in range(b[i][1]):
        bs.append(b[i][0])                        

print("Plotting)")
fig, (ax1, ax2) = plt.subplots(2, 1)

            ######## Histogram of magnitude ########

#Find number of bins
highbin = int(np.round(max(bs)) + 1)

#Plot magnitudes
ax1.hist(bs, bins = range(0, highbin), histtype = 'step', color = "w", edgecolor = "black")

#Title
ax1.set_title("Magnetic field distribution")
ax1.set_xlabel("|B| (nT)")
ax1.set_ylabel("Frequency")

            ######## x- and y- histogram ########

#Find number of bins
xmin = int(np.round(min(bxs)) - 1)
xmax = int(np.round(max(bxs)) + 1)
ymin = int(np.round(min(bys)) - 1)
ymax = int(np.round(max(bys)) + 1)


#Plot magnitudes
h = ax2.hist2d(bxs, bys, bins = (range(xmin, xmax), range(ymin, ymax)), cmap = "binary")
fig.colorbar(h[3], ax=ax2)

#Labels
ax2.set_xlabel("Bx (nT)")
ax2.set_ylabel("By (nT)")

plt.show()