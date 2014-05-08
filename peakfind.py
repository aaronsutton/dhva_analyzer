'''
Created on Feb 24, 2012

@author: asutton
Code snippets for gaussian fitting taken from http://www.krioma.net/blog/2011/12/gaussian_fitting_in_python.php
'''
#from pylab import *
from scipy.optimize import leastsq
import select_data
import matplotlib.pyplot as plt
from numpy import *
import warnings

def peakfind(freq,FFT,fig):
    keepgoing = 3
    dHvApeaks = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        while (keepgoing == 3):
            testpoints = plt.ginput(n=3, timeout=0, show_clicks=True, mouse_add=1, mouse_pop=3, mouse_stop=2)
            xclick_unsorted = map(lambda xclick_unsorted: xclick_unsorted[0],testpoints)
            yclick_unsorted = map(lambda xclick_unsorted: xclick_unsorted[1],testpoints)
            keepgoing = len(xclick_unsorted)
            if (keepgoing == 3):
                points = zip(xclick_unsorted,yclick_unsorted)
                sorted_points = sorted(points)
                xclick = [point[0] for point in sorted_points]
                yclick = [point[1] for point in sorted_points]
                xseldata,yseldata,blank = select_data.select_data(freq,FFT,zeros(len(freq)),xclick[0],xclick[2])
                guess_a = yclick[1]
    #print(guess_a)
    #figure(2)
    #plot(xseldata,yseldata,'y')
    #draw()
    
    #Playing with gaussian fit
                gauss_fit = lambda p, x: p[0]*(1/sqrt(2*pi*(p[2]**2)))*exp(-(x-p[1])**2/(2*p[2]**2))
                e_gauss_fit = lambda p, x, y: (gauss_fit(p,x) -y)
                x_pos = double(xseldata)
                y_power = double(yseldata) 
    
                v0 = [guess_a,mean(x_pos),1.0] #inital guesses for Gaussian Fit. $just do it around the peak
                out = leastsq(e_gauss_fit, v0[:], args=(x_pos, y_power), maxfev=100000, full_output=1) #Gauss Fit
                v = out[0] #fit parammeters out
                covar = out[1] #covariance matrix output
    
                xxx = arange(min(x_pos),max(x_pos),x_pos[1]-x_pos[0])
                ccc = gauss_fit(v,xxx) # this will only work if the units are pixel and not wavelength
    
                fig.plot(xxx,ccc,'b--')
                plt.axvline(x=xxx[where(ccc == max(ccc))[0]][0],color='r')
                plt.draw()
        
    #fig = figure(3) #make a plot
    #ax1 = fig.add_subplot(111)
    #ax1.plot(x_pos,y_power,'gs') #spectrum
    #ax1.plot(xxx,ccc,'b--') #fitted spectrum
    #ax1.axvline(x=xxx[where(ccc == max(ccc))[0]][0],color='r') #max position in data
    #setp(gca(), ylabel="power", xlabel="pixel position")
    #savefig("plotfitting.png")
    
            #print "p[0], a: ", v[0]
            #print "peak height: ", max(ccc)
            #print "p[1], mu: ", v[1]
                dHvApeaks[len(dHvApeaks):]=[(v[1],max(ccc))]
    #print(dHvApeaks)
    return dHvApeaks
