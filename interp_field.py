'''
Modified from Stephen Julian's dhva_routines module
'''
from numpy.fft import fft
import numpy
from numpy import arange,array,average,diff,sqrt,take,argsort,sort,transpose,ones,add
from numpy.linalg import solve
from math import sin,sqrt,pi
from string import split,atof

def next_pow_2(N):
    i = 0
    two_to_the_i = 1
    while N>two_to_the_i:
        i += 1
        two_to_the_i *= 2
    return i
def Sum_i(f):
    return add.reduce(f,0)
def Sum_j(f):
    return add.reduce(f,1)
def window(N):
    return arange(1,N+1,1)*arange(N,0,-1)
def four_point(x,y,x0):
        result = 0.0e+00
        result += (x0 - x[1])*( x0 - x[2])*(x0 - x[3])/( (x[0] - x[1])*(x[0] - x[2])*(x[0] - x[3]))*y[0]
        result += (x0 - x[0])*(x0 - x[2])*(x0 - x[3])/( (x[1] - x[0])*(x[1] - x[2])*(x[1] - x[3]))*y[1]
        result += (x0 - x[0])*(x0 - x[1])*(x0 - x[3])/( (x[2] - x[0])*(x[2] - x[1])*(x[2] - x[3]))*y[2]
        result += (x0 - x[0])*(x0 - x[1])*(x0 - x[2])/( (x[3] - x[0])*(x[3] - x[1])*(x[3] - x[2]))*y[3]
        return result

def inv_field(x_i,B_i):
    Pow_2 = next_pow_2( len(B_i) )   #next_pow_2 is defined at start of this file
    N = pow(2,Pow_2)
    I_B_min = 1.0/max(B_i)
    I_B_max = 1.0/min(B_i)
    Delta_I_B = (I_B_max - I_B_min)/N
    tmpX = []
    tmpIB = []
    tmpIB1 = sort(1.0/B_i)
    next_inverse_field = I_B_min
    current_index = 0
    for i in range(0,N-1):
        tmpIB.append( next_inverse_field )
        while ( tmpIB[i] ) >= tmpIB1[current_index]:
            current_index += 1 
        if current_index < ( len(tmpIB1) ):
            index = len(B_i)-1  - current_index
            if (index <= 1) | (index >= len(B_i)-2):
                tmpX.append(x_i[index] + (1.0/tmpIB[i] - B_i[index])*(x_i[index+1] - x_i[index] )/(B_i[index+1] - B_i[index] ) )
            else:
                tmpX.append(  four_point( B_i[index-1:index+3] , x_i[index-1:index+3] , 1.0/tmpIB[i] ))
        next_inverse_field += Delta_I_B
    IB_i = array(tmpIB)
    Ix_i = array(tmpX)
    return Ix_i, IB_i, Delta_I_B