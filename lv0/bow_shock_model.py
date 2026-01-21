'''
Bow shock model, taken from the experimental fit data from Hall et al. (2016) Annual variations in the Martian bow shock location as observed by the Mars Express mission.

Note: this model is in [aberrated MSO coordinates]; this is a coordinate system rotated about the Z-axis by 4 degrees from the typical MSO coordinates, to account for the angle of solar wind incidence at Mars.
      To use this model with data in MSO coordinates, the inverse 4 degree rotation must be applied first.
'''

import numpy as np

def is_in_solarwind(x, y, z):
      '''
      Inputs: position
      Outputs: bool (True: position is outside the magnetosphere)
      '''
      #Get rotation angle in radians
      rotang = 4*np.pi/180
      rot_matrix = np.array([[np.cos(rotang), -np.sin(rotang), 0], 
                          [np.sin(rotang), np.cos(rotang), 0], 
                          [0, 0, 1]])
      
      #Position in aberrated MSO coordinates
      pos = np.matmul(rot_matrix, np.array([x, y, z]))

      #Shift coordinate origin to focus of conic section
      pos -= np.array([x0*3389.5, 0, 0])

      #Distance from focus of conic section
      r = np.linalg.norm(pos)
      
      #Maven angle above x-axis
      theta = np.acos(pos[0]/r)

      #Bow shock distance for the angle
      r_bs = L/(1+e*np.cos(theta))

      #Extra 10% margin of error
      r_bs *= 1.1

      #Convert to km
      r_bs *= 3389.5

      #Returns True if MAVEN is in the solar wind
      return(r>r_bs)
    


            ######## Bow shock parameters ########

global x0
global L
global e
global Rss
global Rtd

x0 = 0.74
L = 1.82
e = 1.01
Rss = 1.65
Rtd = 2.46

            ######## Model generation ########

#Angles between 0 and 135 degrees
theta = np.linspace(0, 3*np.pi/4, 100)

#Calculates corresponding radial displacement from (x, rho) = (x_0, 0)
r = L/(1+e*np.cos(theta))

#x-coordinates relative to (x_0, 0)
xrel= r*np.cos(theta)

#Shift x-coordinates to MSO origin
x = xrel + x0

#rho-coordinates relative to (x_0, 0)
rho = r*np.sin(theta)