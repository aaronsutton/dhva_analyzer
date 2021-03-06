'''
Created on May 11, 2011

@author: asutton
'''
import numpy as np
#from pylab import *

def take_fft(y,power,delta_freq):
    pow_res = np.power(2,power)
    temp_fft = np.fft.fft(y,pow_res)
    temp_y = np.abs(temp_fft)
    temp_x = np.array(range(len(temp_y)/2))
    freq_array = delta_freq*temp_x/len(temp_y)
    fft_array = temp_y[0:len(temp_y)/2]
    return freq_array, fft_array
