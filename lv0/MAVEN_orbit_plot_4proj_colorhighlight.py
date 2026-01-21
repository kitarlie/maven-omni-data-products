'''
Author: Charlie Proudfoot
Last updated: 21/10/25

Takes a day of MAVEN data and outputs a graph of its orbit projected onto the MSO X-Y, X-Z, Y-Z and X-ρ planes. Also plots a modelled bow shock based on the Hall et al. (2016) conic fit model.
'''

from spacepy import pycdf
import matplotlib.pyplot as plt
import numpy as np
import bow_shock_model

from bow_shock_model import x as bowx
bowx = bowx * 3389.5
from bow_shock_model import rho as bowrho
bowrho = bowrho * 3389.5
from bow_shock_model import Rtd
Rtd = Rtd * 3389.5

            ######### Get data ##########

cdf = pycdf.CDF("S:/data/maven/maven/data/sci/kp/cdfs/mvn_insitu_kp-4sec_20140410_v13_r03.cdf")

#Components of MAVEN position vector in Mars-Solar-Orbital coordinates
xs_in = []
ys_in = []
zs_in = []

xs_out = []
ys_out = []
zs_out = []

#Extracts position vector
for i in range(0, len(cdf['SPICE_spacecraft_MSO'])):
    x = cdf['SPICE_spacecraft_MSO'][i][0]
    y = cdf['SPICE_spacecraft_MSO'][i][1]
    z = cdf['SPICE_spacecraft_MSO'][i][2]
    print(cdf['SPICE_spacecraft_MSO'][i])

    if bow_shock_model.is_in_solarwind(x, y, z) == True:
        xs_out.append(cdf['SPICE_spacecraft_MSO'][i][0])
        ys_out.append(cdf['SPICE_spacecraft_MSO'][i][1])
        zs_out.append(cdf['SPICE_spacecraft_MSO'][i][2])
    else:
        xs_in.append(cdf['SPICE_spacecraft_MSO'][i][0])
        ys_in.append(cdf['SPICE_spacecraft_MSO'][i][1])
        zs_in.append(cdf['SPICE_spacecraft_MSO'][i][2])



#Rho coordinate
rhos_in = [np.sqrt(ys_in[i]**2 + zs_in[i]**2) for i in range(len(ys_in))]
rhos_out = [np.sqrt(ys_out[i]**2 + zs_out[i]**2) for i in range(len(ys_out))]

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

fig.suptitle("April 10th 2014")

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
ax1.plot(xs_out, ys_out, color = 'g')
ax1.plot(xs_in, ys_in)

#Plot sphere
ax1.plot(x, y, color = 'r')

#Plot bow shock
ax1.plot(bowx, bowrho, color = 'w', linestyle = None)
ax1.plot(bowx, -bowrho, color = 'w', linestyle = None)



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
ax2.plot(xs_out, zs_out, color = 'g')
ax2.plot(xs_in, zs_in)

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
ax3.plot(ys_out, zs_out, color = 'g', linestyle = None)
ax3.plot(ys_in, zs_in, linestyle = None)

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
ax4.plot(xs_out, rhos_out, color = 'g')
ax4.plot(xs_in, rhos_in)

#Plot sphere
ax4.plot(x, y, color = 'r')

#Plot bow shock
ax4.plot(bowx, bowrho, color = 'w')



plt.show()