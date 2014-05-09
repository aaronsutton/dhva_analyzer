from pycdf import *
import string,os

for name in os.listdir('./'):
    if (name[0] == '2')&(name[-1] == 'c'):
        #   test = 0
        print name[0:-3]
        nc = CDF(name)
        ncattr = nc.attributes()   # dictionary of attributes
        vardict = nc.variables()   # dictionary of variables
        varnames = vardict.keys()    # list of variable 
        printnames = 0
        if printnames:
            print varnames, ncattr
        printvars = 1
        if printvars:
            outstr = '# '+ ncattr['Comments'] + ', T_target ' + str(nc.var('FinalT')[0]) + ', HSweepRate ' + str(nc.var('HSweepRate')[0])
            print outstr
# pylab.plot(B,X)
# pylab.show()

