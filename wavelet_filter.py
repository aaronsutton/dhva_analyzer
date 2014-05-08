'''
Created on May 3, 2011

@author: asutton
'''
import numpy as np
import pywt
#from pylab import *
import return_DataToPlot as DP

#CurrentH,CurrentT,A1X,A1Y,A2X,A2Y,E,F = DP.return_DataToPlot('2011_03_28_04_BiSe_001.nc')
#decomp_lev = 4
#type = 'coif2'
def wavelet_filter(A1X, decomp_lev, type):
    if isinstance(decomp_lev, int) and decomp_lev > 0:
        #print(pywt.wavelist('bior'))
        decomp = pywt.wavedec(A1X[:], type, level=decomp_lev)
      
        sigma_j = np.median(abs(decomp[-1]))/0.6745
        threshold_j = sigma_j*np.sqrt(2*np.log(len(A1X)))
    
        for i in range(decomp_lev):
            decomp[i + 1] = pywt.thresholding.less(decomp[i+1],threshold_j)
            decomp[i + 1] = pywt.thresholding.greater(decomp[i+1],-threshold_j)
        
        filt_A1X = pywt.waverec(decomp, type)
  

        return filt_A1X
        
    else:
        print('invalid')
