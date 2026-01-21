'''
Author: Charlie Proudfoot
Last updated: 21/10/25

Takes a day of MAVEN data and outputs a graph of its orbit projected onto the MSO X-Y, X-Z, Y-Z and X-ρ planes. Also plots a modelled bow shock based on the Hall et al. (2016) conic fit model.
'''

from spacepy import pycdf
import matplotlib.pyplot as plt
import numpy as np

from bow_shock_model import x as bowx
bowx = bowx * 3389.5
from bow_shock_model import rho as bowrho
bowrho = bowrho * 3389.5
from bow_shock_model import Rtd
Rtd = Rtd * 3389.5

            ######### Get data ##########

cdf = pycdf.CDF('C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/MAVEN-data/mvn_insitu_kp-4sec_20181030_v19_r01.cdf')

#Components of MAVEN position vector in Mars-Solar-Orbital coordinates
xs = []
ys = []
zs = []

#Extracts position vector
for i in range(0, 11677):
    xs.append(cdf['SPICE_spacecraft_MSO'][i][0])
    ys.append(cdf['SPICE_spacecraft_MSO'][i][1])
    zs.append(cdf['SPICE_spacecraft_MSO'][i][2])

#Rho coordinate
rhos = [np.sqrt(ys[i]**2 + zs[i]**2) for i in range(len(ys))]

#Creates sphere representing Mars
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, np.pi, 100)
r = 3389.5

#Convert to Cartesian coords
x = r * np.cos(theta)
y = r * np.sin(theta)



#Set up figure and subplot axes
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig.tight_layout()



            ######### X-Y projection ##########

#Create square subplot axis
ax1.set_aspect('equal')

#Set background colour to black
ax1.set_facecolor('xkcd:black')

#Consistent axis limits so sphere plot is not stretched
ax1.set_xlim(-10000, 10000)
ax1.set_ylim(-10000, 10000)

#Title and axis labels/ticks
ax1.set_title("X-Y projection")
ax1.set_xlabel("X (km)")
ax1.set_ylabel("Y (km)")
ax1.set_xticks([-10000, -5000, 0, 5000, 10000])
ax1.set_yticks([-10000, -5000, 0, 5000, 10000])

#Plots MAVEN orbit
ax1.plot(xs, ys)

#Plot sphere
ax1.plot(x, y, color = 'r')

#Plot bow shock
ax1.plot(bowx, bowrho, color = 'w')
ax1.plot(bowx, -bowrho, color = 'w')



            ######### X-Z projection ##########

#Create square subplot axis
ax2.set_aspect('equal')

#Set background colour to black
ax2.set_facecolor('xkcd:black')

#Consistent axis limits so sphere plot is not stretched
ax2.set_xlim(-10000, 10000)
ax2.set_ylim(-10000, 10000)

#Title and axis labels
ax2.set_title("X-Z projection")
ax2.set_xlabel("X (km)")
ax2.set_ylabel("Z (km)")
ax2.set_xticks([-10000, -5000, 0, 5000, 10000])
ax2.set_yticks([-10000, -5000, 0, 5000, 10000])

#Plots MAVEN orbit
ax2.plot(xs, zs)

#Plot sphere
ax2.plot(x, y, color = 'r')

#Plot bow shock
ax2.plot(bowx, bowrho, color = 'w')
ax2.plot(bowx, -bowrho, color = 'w')



            ######### Y-Z projection ##########

#Create square subplot axis
ax3.set_aspect('equal')

#Set background colour to black
ax3.set_facecolor('xkcd:black')

#Consistent axis limits so sphere plot is not stretched
ax3.set_xlim(-10000, 10000)
ax3.set_ylim(-10000, 10000)

#Title and axis labels
ax3.set_title("Y-Z projection")
ax3.set_xlabel("Y (km)")
ax3.set_ylabel("Z (km)")
ax3.set_xticks([-10000, -5000, 0, 5000, 10000])
ax3.set_yticks([-10000, -5000, 0, 5000, 10000])

#Plots MAVEN orbit
ax3.plot(ys, zs)

#Plot sphere
ax3.plot(x, y, color = 'r')

#Create a circle representing the bow shock in the y-z plane
bowyz_x = Rtd*np.cos(theta)
bowyz_y = Rtd*np.sin(theta)

#Plots bow shock
ax3.plot(bowyz_x, bowyz_y, color = 'w')


            ######### X-rho projection ##########

#Create square subplot axis
ax4.set_aspect('equal')

#Set background colour to black
ax4.set_facecolor('xkcd:black')

#Consistent axis limits so sphere plot is not stretched
ax4.set_xlim(-10000, 10000)
ax4.set_ylim(0, 10000)

#Title and axis labels
ax4.set_title("X-ρ projection")
ax4.set_xlabel("X (km)")
ax4.set_ylabel("ρ (km)")
ax4.set_xticks([-10000, -5000, 0, 5000, 10000])
ax4.set_yticks([0, 5000, 10000])

#Plots MAVEN orbit
ax4.plot(xs, rhos)

#Plot sphere
ax4.plot(x, y, color = 'r')

#Plot bow shock
ax4.plot(bowx, bowrho, color = 'w')



plt.show()