'''
Created on 2011-05-12

@author: asutton
'''
#from pylab import *
import numpy as np
from itertools import count,izip

def find_angle(A1X,A1Y):
    ratio = A1X[-1]/A1Y[-1]
    ratio = -1*ratio
    calc_theta_deg = np.arctan(ratio)*180/np.pi
    temp_theta=[]
    temp_value=[]
    for index in range(int(round(calc_theta_deg - 10,0)), int(round(calc_theta_deg + 10,0)),1):
        theta_deg = index
        theta_rad = np.pi*theta_deg/180
        UnSortSignalA = A1X*np.cos(theta_rad)+A1Y*np.sin(theta_rad)
        result = np.average(abs(UnSortSignalA))
        temp_value = np.append(temp_value,result)
        temp_theta = np.append(temp_theta,theta_deg)
        #print(result,theta_deg)

    min_value,min_index = min(izip(temp_value,count()))
    #print(min_value,min_index)
    #Something wonky here. Phase is totally wrong. Try to remove 90 degree shift.
    #theta_deg = temp_theta[min_index]
    #theta_deg = temp_theta[min_index] + 90
    theta_deg = 0
    theta_rad = np.pi*theta_deg/180
    UnSortSignalA = A1X*np.cos(theta_rad)+A1Y*np.sin(theta_rad)
    UnSortSignalAY = A1Y
    #Try this instead of phase.
    #UnSortSignalA = np.sqrt(A1X**2 + A1Y**2)
    
    #print(theta_deg)
    return UnSortSignalA,UnSortSignalAY
