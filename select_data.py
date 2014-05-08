'''
Created on May 11, 2011

@author: asutton
'''
from numpy import *
#from pylab import *

def select_data(field,x,y,min,max):
    temp_field = []
    temp_x = []
    temp_y = []
    for i in range(0,len(field)):
        if (field[i]) > min and (field[i]) < max:
            temp_field = append(temp_field,field[i])
            temp_x = append(temp_x,x[i])
            temp_y = append(temp_y,y[i])
            
    return temp_field, temp_x, temp_y
