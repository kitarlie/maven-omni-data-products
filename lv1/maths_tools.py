'''
Contains the following handy dandy maths tools:

    sign(x): returns the sign of a number x (+1 or -1)
    round_half_int(x): returns the half-integer closest to x
    vector_angle(a,b): returns the angle between vectors a and b in degrees
'''

from math import trunc
import numpy as np
from scipy.optimize import minimize

def sign(x):
    '''
    Returns 1 if x>0, and -1 if x<0
    '''
    return x/abs(x)

def round_half_int(x):
    '''
    Returns the closest half-integer to the input x
    '''
    #Decimal part of the number
    y = (x - trunc(x))**2
    if y >= 0.75**2:
        return(trunc(x) + sign(x))
    elif y < 0.25**2:
        return(trunc(x))
    else:
        return(trunc(x) + 0.5*sign(x))
    

def vector_angle(a, b):
    '''
    Returns the angle between vectors a and b, in degrees
    a.b = abcos(theta)
    '''

    return 180/np.pi * np.acos((a[0]*b[0] + a[1]*b[1] + a[2]*b[2])/(np.linalg.norm(a)*np.linalg.norm(b)))

def resduals_squared(m, matrix):
    sum = 0
    for i in range(10):
        for j in range(10):
            sum += matrix[i][j]*abs(((i/2 - 5) - m[0]*(j/2 - 5) - m[1]))
    return sum


def best_fit(matrix):
    fun=lambda m: resduals_squared(m, matrix)
    optimizeResult = minimize(fun, [-1, 0])

    print(optimizeResult.x)

    return optimizeResult.x[0], optimizeResult.x[1]

def median(matrix):
    medians = []
    for j in range(80):
        sum = 0
        for i in range(80):
            sum += matrix[i][j]
        count = 0
        for i in range(80):
            count += matrix[i][j]
            if count > sum/2:
                medians.append(i/2 - 20)
                break
    return medians


    