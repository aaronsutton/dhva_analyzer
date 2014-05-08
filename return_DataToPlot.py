'''
Created on Apr 29, 2011

@author: asutton
'''
import netCDF4
#python netcdf library
from numpy import *
#import pylab
import os, string

def return_DataToPlot(path,name):
    os.chdir(path)
    plotvariables = dict()
    #print('starting...')
    #if (name[0] == '2')&(name[-1] == 'c'):
    if (name[-1] == 'c'):
        nc = netCDF4.Dataset(name, 'r')
        plotvariables['B'] = nc.variables['CurrentH']
        plotvariables['T'] = nc.variables['CurrentT']
        plotvariables['A1X'] = nc.variables['A1X']
        plotvariables['A1Y'] = nc.variables['A1Y']
        plotvariables['A2X'] = nc.variables['A2X']
        plotvariables['A2Y'] = nc.variables['A2Y']
        plotvariables['B1X'] = nc.variables['B1X']
        plotvariables['B1Y'] = nc.variables['B1Y']
        plotvariables['B2X'] = nc.variables['B2X']
        plotvariables['B2Y'] = nc.variables['B2Y']
        plotvariables['C1X'] = nc.variables['C1X']
        plotvariables['C1Y'] = nc.variables['C1Y']
        plotvariables['C2X'] = nc.variables['C2X']
        plotvariables['C2Y'] = nc.variables['C2Y']
        plotvariables['E'] = nc.variables['EVoltage']
        plotvariables['F'] = nc.variables['FVoltage']        
        #return B,T,A1X,A1Y,A2X,A2Y,B1X,B1Y,B2X,B2Y,C1X,C1Y,C2X,C2Y,E,F,nc
        return plotvariables,nc
        #nc.close()
        #print('done getting data')
