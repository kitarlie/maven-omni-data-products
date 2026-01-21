'''
For checking whether Earth and Mars lie on the same Parker field line (or within a certain angle of the same field line).
Running this file will write the data file containing the conjunction angles.
'''

from astropy.time import Time
from datetime import date, timedelta
from astropy import units as u
from astropy.coordinates import get_body_barycentric, Angle
import numpy as np
import csv

def time_string(year, day):
    '''
    Parameters:
        daystring (str): the date in format "YYYYMMDD" 
        i: the current index of the CDF file
        i_max: the final index of the CDF file 

    Returns:   
        The date and time in format "YYYY-MM-DD hh:mm"
    '''
    #Day 1 of the year
    strt_date = date(int(year), 1, 1)

    #Convert to date
    res_date = strt_date + timedelta(days=int(day) - 1)
    res = res_date.strftime("%Y-%m-%d")

    #Return date and time in form "YYYY-MM-DD 00:00"
    return(res + " 00:00")

def time_string_minsec(year, day, hour, min):
    #Day 1 of the year
    strt_date = date(year, 1, 1)

    hour = str(hour)
    if len(hour) == 1:
        hour = "0" + hour
    min = str(min)
    if len(min) == 1:
        min = "0" + min

    #Convert to date
    res_date = strt_date + timedelta(days=int(day) - 1)
    res = res_date.strftime("%Y-%m-%d")

    #Return date and time in form "YYYY-MM-DD hh:mm"
    return(res + " " + hour + ":" + min)


def is_mars_aligned(t):
    '''
    Inputs: t: the date and time
    Returns: delta: the angle (in degrees) between the Parker spiral field lines associated with Earth and Mars, extrapolated back to the Earth's orbit.
    '''

    t = Time(t)

    half_turn = Angle(np.pi, unit = u.rad)
    full_turn = Angle(2*np.pi, unit = u.rad)
    zero_angle = Angle(0, unit = u.rad)

    #Heliocentric coordinates of Mars and Earth
    mars = (get_body_barycentric('mars', t) - get_body_barycentric('sun', t))
    earth = (get_body_barycentric('earth', t) - get_body_barycentric('sun', t))

    mars_r = mars.norm()
    earth_r = earth.norm()
    
    #Mars' heliospheric longitude
    mars_t = np.arctan2(mars.y, mars.x)

    #The angle relative to the x-axis of the point IMF field line connecting the Sun to Mars, coinciding with Earth's orbit
    mars_t_e = (2*np.pi/(25*24*60*60 * 440000))*149597871*(mars_r - earth_r)

    #Extract numerical value
    mars_t_e = mars_t_e.to_string()
    mars_t_e = mars_t_e.split(' ')
    mars_t_e = float(mars_t_e[0])

    #Create angle object
    mars_t_e = mars_t + Angle(mars_t_e, unit = u.rad)

    #The angle relative to the x-axis of the IMF field line connecting the Sun to Earth, at Earth's orbit
    earth_t = np.arctan2(earth.y, earth.x)

    #Difference between angles
    delta = earth_t - mars_t_e

    if delta < zero_angle:
        delta = -delta

    #Changes reflex angle to complementary acute/obtuse angle
    if delta > half_turn:
        delta = full_turn - delta

    #Extract numerical value
    delta = delta.to_string()
    delta = delta.split(' ')
    delta = float(delta[0])
    
    return delta*180/np.pi

def get_mars_time(omni_time, sw_velocity):
    """Uses the Vennerstrom propagation model to get the propagation time at Mars

    Args:
        omni_time (array): [year, day, hour, minute]
        sw_velocity (float): the solar wind flow speed in km/s
    """

    t = time_string_minsec(int(omni_time[0]), int(omni_time[1]), int(omni_time[2]), int(omni_time[3]))
    t = Time(t)


    half_turn = Angle(np.pi, unit = u.rad)
    full_turn = Angle(2*np.pi, unit = u.rad)
    zero_angle = Angle(0, unit = u.rad)

    #Heliocentric coordinates of Mars and Earth
    mars = (get_body_barycentric('mars', t) - get_body_barycentric('sun', t))
    earth = (get_body_barycentric('earth', t) - get_body_barycentric('sun', t))

    mars_r = mars.norm()
    earth_r = earth.norm()

    delta_r = mars_r - earth_r
    
    #Heliospheric longitude of Mars
    mars_t = np.arctan2(mars.y, mars.x)

    #Heliospheric longitude of Earth
    earth_t = np.arctan2(earth.y, earth.x)

    delta = mars_t - earth_t

    #Makes all angles positive (i.e. changes direction of negative angle separation)
    if delta < zero_angle:
        delta = -delta

    #Changes reflex angle to complementary acute/obtuse angle
    if delta > half_turn:
        delta = full_turn - delta

    #Extract numerical values
    delta = delta.to_string()
    delta = delta.split(' ')
    delta = float(delta[0])


    delta_r = delta_r.to_string()
    delta_r = delta_r.split(' ')
    delta_r = float(delta_r[0])

    omega = 2*np.pi/(25*24*60*60)

    #Vennerstrom time delta (using 1AU = 149597871km)
    dt = 149597871*delta_r/sw_velocity + delta_r/omega

    #Calculate changes in day, minute and hour
    dday = int(dt/(24*60*60))
    dt -= dday*24*60*60
    dhour = int(dt/(60*60))
    dt -= dhour*60*60
    dmin = int(dt/60)
    dt -= dmin*60
    ds = int(dt)

    year = omni_time[0]
    
    #Handle time overflows (e.g. 25 hours = 1 day + 1 hour)
    n_min = omni_time[3] + dmin
    if n_min >= 60:
        dhour += 1
        n_min -= 60

    n_hour = omni_time[2] + dhour
    if n_hour >= 24:
        dday += 1
        n_hour -= 24

    n_day = omni_time[1]+dday
    #Leap year
    if n_day > 366 and omni_time[0]%4 == 0:
        year += 1
        n_day -= 366
    elif n_day > 365:
        year += 1
        n_day -= 365
   
    return [year, n_day, n_hour, n_min, ds]


#Create the data file with conjunction angles
'''
with open("C:/Users/charl/Documents/Uni/Part II/Year 4/PHYS450/Data/conjunction-angles.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Year", "Day", "Conjunction angle"])
    for year in range(1981, 2026):
        for day in range(1, 367):
            time = time_string(year, day)
            delta = is_mars_aligned(time)
            csvwriter.writerow([year, day, delta])
'''