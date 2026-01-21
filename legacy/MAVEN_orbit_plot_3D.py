from spacepy import pycdf
import matplotlib.pyplot as plt
import numpy as np

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

#Sets up 3D axis
fig = plt.figure()
ax = fig.add_subplot(projection = '3d')
ax.set_aspect('equal')

#Remove axis and set background colour to black
ax._axis3don = False
ax.set_facecolor('xkcd:black')

#Consistent axis limits so sphere plot is not stretched
ax.set_xlim(-10000, 10000)
ax.set_ylim(-10000, 10000)
ax.set_zlim(-10000, 10000)

#Plots MAVEN orbit
ax.scatter(xs, ys, zs)

#Creates sphere representing Mars
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, np.pi, 50)
theta, phi = np.meshgrid(theta, phi)
r = 3389.5

#Convert to Cartesian coords
x = r * np.sin(phi) * np.cos(theta)
y = r * np.sin(phi) * np.sin(theta)
z = r * np.cos(phi)
 
#Plot sphere
ax.plot_surface(x, y, z, color = 'r')

plt.show()