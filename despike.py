import numpy 
from numpy.linalg import solve
import string,os
import sys
from math import pi,sin,cos,sqrt

def four_point(x,y,x0):    # four point interpolation
    result = 0.0e+00
    result += (x0 - x[1])*( x0 - x[2])*(x0 - x[3])/( (x[0] - x[1])*(x[0] - x[2])*(x[0] - x[3]))*y[0]
    result += (x0 - x[0])*(x0 - x[2])*(x0 - x[3])/( (x[1] - x[0])*(x[1] - x[2])*(x[1] - x[3]))*y[1]
    result += (x0 - x[0])*(x0 - x[1])*(x0 - x[3])/( (x[2] - x[0])*(x[2] - x[1])*(x[2] - x[3]))*y[2]
    result += (x0 - x[0])*(x0 - x[1])*(x0 - x[2])/( (x[3] - x[0])*(x[3] - x[1])*(x[3] - x[2]))*y[3]
    return result

def Sum_i(f):
    return numpy.add.reduce(f,0)

def fit_polynomial(N,x_i,y_i):     # this came from remove_background in spectrum.py
        # x_i and y_i are Numeric arrays
    tmp = numpy.ones( len(x_i), numpy.float32 )
    X = []
    Y = []
    X_vec = []
    for i in range(0,2*N+1):
        X.append( Sum_i( tmp ) )
        if i<=N:
            Y.append( Sum_i(y_i*tmp) )
            X_vec.append( tmp )
        tmp = tmp*x_i
    X_0 = []
    lo = 0
    hi = N
    for i in range(0,N+1):
        X_0.append( numpy.array( X[lo:hi+1] ) )
        lo = lo + 1
        hi = hi + 1
    X_i_j = numpy.array(X_0)
    Y_i = numpy.array(Y)
    a_i = solve( X_i_j , Y_i )
    X_vec_i = numpy.array(X_vec)
    y_removed_i = 1.0*y_i    # create a new array
    for i in range(0,N+1):
        y_removed_i = y_removed_i - a_i[i]*X_vec_i[i]
    return numpy.array(y_removed_i),numpy.array(a_i)

test = 1
for name in os.listdir('./'):
# print name[-3:-1]
    if name == '2009_07_06_02_YbRh2Si22_000.dat':
# if (name[-3:-1]=='da') & (name[0:4]=='2008') & (test==1):
#   test = 0
        infile = open(name,"r")

        Bt = []
        xt = []
        yt = []
        print name[0:-3]
        for line in infile.readlines():
            if line[0]<>'#':
                tmp = string.split(line)
                Btmp,xtmp,ytmp = tmp[0],tmp[3],tmp[4]
                Bt.append( string.atof(Btmp) )
                xt.append( string.atof(xtmp) )
                yt.append( string.atof(ytmp) )

        B_i = numpy.array( Bt )
        x_i = numpy.array( xt )
        y_i = numpy.array( yt )

        SPIKEWIDTH = 9
        BGW = 35

# combine phases
        theta = (0.0+0.37)*pi
        R_i = cos(theta)*x_i + sin(theta)*y_i 

# remove background

        R_new,garb = fit_polynomial(3,B_i,R_i)
        R_i = 1.0*R_new

# now despike
        ynew_i = 1.0*R_i
        for i in range( BGW/2, len(x_i)-BGW/2+1):  
            ysec_i = R_i[i-BGW/2 : i+BGW/2]
            Bsec_i = B_i[i-BGW/2 : i+BGW/2]
            dy_i,a_i = fit_polynomial(2,Bsec_i,ysec_i)

# calculate sigma
            sum_dy = numpy.sum( dy_i)
            sigma = sqrt(  numpy.sum( dy_i*dy_i)/BGW -  sum_dy*sum_dy/BGW )



# now find and fix spikes
            if abs(dy_i[BGW/2]) > 2.5*sigma:   # then it's a spike
                print "# spike at ",B_i[i],R_i[i]
                k1 = i-SPIKEWIDTH-1
                k2 = i+SPIKEWIDTH+1
#      x_interp = [ B_i[k1-1],B_i[k1],B_i[k2],B_i[k2+1] ]
#      y_interp = [ R_i[k1-1],R_i[k1],R_i[k2],R_i[k2+1] ]
#      ynew_i[i] =   four_point(x_interp,y_interp,B_i[i] )
                x1 = B_i[k1-6:k1]
                y1 = R_i[k1-6:k1]
                x2 = B_i[k2:k2+6]
                y2 = R_i[k2:k2+6]
                x_interp = numpy.concatenate( (x1,x2), axis=0)
                y_interp = numpy.concatenate( (y1,y2), axis=0)
                garb,a1_i = fit_polynomial(2,x_interp,y_interp)
#      print x_interp,y_interp,garb
                ynew_i[i] = 0
                for n in range(0,3):
                    ynew_i[i] += a1_i[n]*pow(B_i[i],n)
# try to use polynomial interpolation to improve the despiking



        outfile = open(name[0:-3]+'cor','w')
        for i in range(0,len(y_i)):
            outstr = str(B_i[i]) + ' ' + str(R_i[i]) + ' ' + str(ynew_i[i]) + '\n'
            outfile.write(outstr)
        infile.close()
        outfile.close()

