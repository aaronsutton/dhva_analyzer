#Modified from Stephen Julian's netCDF dHvA analysis modules

import netCDF4 #python netcdf library
from numpy import *
#import pylab
import os, string

def convert_CDF(path):
    #netCDF4 = netCDF4 #required for unknown reason
    os.chdir(path)
    test = 1
    for name in os.listdir('./'):
        if test==1:
            if (name[0] == '2')&(name[-1] == 'c'):   
                # test = 0
                print name[0:-3]
                nc = netCDF4.Dataset(name, 'r')
                ncattr = nc.ncattrs()   # dictionary of attributes
                vardict = nc.variables   # dictionary of variables
                varnames = vardict.keys()    # list of variable 
                printnames = 0
                if printnames:
                    print varnames, ncattr
                printvars = 1
                if printvars:
                    B = nc.variables['CurrentH']
                    T = nc.variables['CurrentT']
                    A1X = nc.variables['A1X']
                    A1Y = nc.variables['A1Y']
                    A2X = nc.variables['A2X']
                    A2Y = nc.variables['A2Y']
                    B1X = nc.variables['B1X']
                    B1Y = nc.variables['B1Y']
                    B2X = nc.variables['B2X']
                    B2Y = nc.variables['B2Y']
                    C1X = nc.variables['C1X']
                    C1Y = nc.variables['C1Y']
                    C2X = nc.variables['C2X']
                    C2Y = nc.variables['C2Y']
                    E = nc.variables['EVoltage']
                    F = nc.variables['FVoltage']
                    fout = open(name[0:-3]+'.dat','w')
                    Comments = getattr(nc,'Comments')
                    FinalT = nc.variables['FinalT']
                    HSweepRate = nc.variables['HSweepRate']
                    outstr = '# '+ Comments + ', T_target ' + str(FinalT[0]) + ', HSweepRate ' + str(HSweepRate[0])
                    print outstr
                    fout.write(outstr)
                    outstr = "#   B    X_1     Y_1    X_2     Y_2     EVoltage   FVoltage "
                    fout.write(outstr)
                    for i in range(0,len(B)):
                        outstr = str(B[i])+'\t'+str(A1X[i])+'\t'+str(A1Y[i])+'\t'+ str(A2X[i])+'\t'+str(A2Y[i])+'\t'+str(B1X[i])+'\t'+str(B1Y[i])+'\t'+ str(B2X[i])+'\t'+str(B2Y[i])+'\t'+str(C1X[i])+'\t'+str(C1Y[i])+'\t'+ str(C2X[i])+'\t'+str(C2Y[i])+str(E[i])+'\t'+str(F[i])+'\n'
                        fout.write(outstr)
                    fout.close()
                    nc.close()
# pylab.plot(B,X)
# pylab.show()

