'''
From Stephen Julian's dHvA analyzing python code.
'''
from numpy.fft import fft
import numpy
from numpy import arange,array,sqrt,take,argsort,sort,transpose,ones,add
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
def remove_background(N,x_i,y_i):
        # x_i and y_i are numpy arrays
        tmp = ones( len(x_i) )
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
                X_0.append( array( X[lo:hi+1] ) )
                lo = lo + 1
                hi = hi + 1
        X_i_j = numpy.array(X_0)
        Y_i = numpy.array(Y)
        a_i = numpy.linalg.solve( X_i_j , Y_i )
        X_vec_i = array(X_vec)
        for i in range(0,N+1):
                y_i = y_i - a_i[i]*X_vec_i[i]
        return numpy.array(y_i),numpy.array(a_i)
def even_interpolate(x_i,y_i,new_x_min,new_x_max,dx):    
    next_x = new_x_min
    current_index = 0
    N = int( (new_x_max - new_x_min)/dx )   #  + 1
    new_x_i = []
    new_y_i = []
    for i in range(0, N-1):
        new_x_i.append( next_x )
        while ( new_x_i[i]  >= x_i[current_index] ):
            current_index += 1
        if current_index < ( len(x_i) ):
            index = current_index     # len(self.B_i)-1  - current_index
            if index > (len(x_i)-2):
                new_y_i.append( y_i[-1])
            else:
                if (index <= 1) | (index >= len(x_i)-2):
                    new_y_i.append( y_i[index] + (new_x_i[i] - x_i[index])*(y_i[index+1] - y_i[index] )/(x_i[index+1] - x_i[index] ) )
                else:
                    new_y_i.append(  four_point( x_i[index-1:index+3] , y_i[index-1:index+3] , new_x_i[i] ))
        next_x += dx
    return new_x_i, new_y_i




class dhva:
    def get_sweep_dirn(self):
        self.B_i1 = self.B_i[1]
        self.B_im = self.B_i[ int(0.5*len(self.B_i)) ]
        self.B_iN = self.B_i[len(self.B_i)-1]
        if self.B_iN < self.B_i1:
            self.sweep_dirn = -1
            tmp = self.B_i1
            self.B_i1 = self.B_iN
            self.B_iN = tmp
            print '#',self.sweep_dirn,"= sweep_dirn"
            del tmp
        else:
            self.sweep_dirn = +1
        print '#',self.B_i1, self.B_im, self.B_iN
    def field_invert(self):
        #    sorting routine
        tmp2 = take( self.x_i,argsort(self.B_i) )  # argsort returns the indices of self.B_i that would
        tmp1 = sort(self.B_i)                    # put it in sorted order. take does what you think
        self.x_i = tmp2                   # it does from the context
        self.B_i = tmp1
        del tmp1,tmp2
        #    field inversion:
        Pow_2 = next_pow_2( len(self.B_i) )   #next_pow_2 is defined at start of this file
        self.N = pow(2,Pow_2)
        I_B_min = 1.0/self.B_i[ len(self.B_i)  - 1]  
        I_B_max = 1.0/self.B_i[0]    
        self.Delta_I_B = (I_B_max - I_B_min)/self.N
        tmpX = []
        tmpIB = []
        tmpIB1 = sort(1.0/self.B_i)

        next_inverse_field = I_B_min
        current_index = 0
        for i in range(0,self.N-1):
            tmpIB.append( next_inverse_field )
            while ( tmpIB[i] ) >= tmpIB1[current_index]:
                current_index += 1 
            if current_index < ( len(tmpIB1) ):
                index = len(self.B_i)-1  - current_index
                if (index <= 1) | (index >= len(self.B_i)-2):
                    tmpX.append( self.x_i[index] + (1.0/tmpIB[i] - self.B_i[index])*(self.x_i[index+1] - self.x_i[index] )/(self.B_i[index+1] - self.B_i[index] ) )
                else:
                    tmpX.append(  four_point( self.B_i[index-1:index+3] , self.x_i[index-1:index+3] , 1.0/tmpIB[i] ))
            next_inverse_field += self.Delta_I_B
        self.IB_i = array(tmpIB)
        self.Ix_i = array(tmpX)
        del tmpX,tmpIB
    def take_fft(self):
        pow2 = 17
        self.freq_i = arange(pow(2,pow2))/(self.Delta_I_B*pow(2,pow2)) # self.N)
        self.y_fft_i = fft(self.Ix_i,pow(2,pow2)) # ,pow(2,pow2) )
        z1 = self.y_fft_i.real*self.y_fft_i.real + self.y_fft_i.imag*self.y_fft_i.imag
#         return numpy.sqrt(z1),self.y_fft_i.real,self.y_fft_i.imag
        scale_factor = 1.0/pow(self.N,3)
        return scale_factor*numpy.sqrt(z1),scale_factor*self.y_fft_i
        del z1#,z3
        
