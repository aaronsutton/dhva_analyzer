'''
Created on Apr 19, 2011
Sorts an array by a specified row.
@author: asutton
'''
import numpy as np

def sortarray(x_in,y_in,row):
    temp = [x_in,y_in]
    temp = zip(*temp)
    temp.sort(key = lambda x: x[0], reverse=False)
    temp = zip(*temp)
    x_out = np.array(temp[0][:])
    y_out = np.array(temp[1][:])
    return x_out, y_out