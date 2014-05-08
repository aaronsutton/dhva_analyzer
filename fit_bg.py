'''
Modified from Kemp Plumb's fit_background.py code
'''
import numpy as np
import fit_wrapper as fw
import copy
#from pylab import *

def polynomial_func(x_data,pars):
    """ defines a polynomial function of order defined by the size of the pars input"""
    f = 0
    for (i,a) in enumerate(pars):
        f += a()*x_data**(i)

    return f

def bg_polynomial(x_data, y_data, p_order,showplot = False):
    """ fits a polynomial of order p_order to x_range, y_range """
    pars = []
    for i in range(p_order):
        pars.append(fw.Parameter(1))

    # fit background 
    bg_fit = fw.fit(polynomial_func, pars, y_data, x_data)
        
    if showplot:
        figure()
        title('polynomial fit to dHvA data')
        plot(x_data, polynomial_func(x_data,pars), 'c-', lw=2)
        plot(x_data,y_data)

    y_data_out = y_data - polynomial_func(x_data,pars)
    return y_data_out, polynomial_func(x_data,pars)
