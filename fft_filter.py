from numpy import fft
import numpy 
import sys,os,string
from math import pi,sqrt
import dhva_routines 
from mpmath import besselj
import pylab as py

a = dhva_routines.dhva()

first_file =1
for name in os.listdir('./'):
    # print name[-3:-1]
    if (name[-3:]=='cor') & (first_file==1):   #  & (name=='2008_05_09_02_PrOs4Sb12_004.cor'):
        # first_file=0    # only do one file until this is working
        infile = open("./"+name,"r")
        Bt = []
        xt = []
        yt = []
        print '#',name[0:-3]
        for line in infile.readlines():
            Btmp,garb,ytmp = string.split(line)
            Bt.append( string.atof(Btmp) )
            yt.append( string.atof(ytmp) )

        a.B_i = numpy.array( Bt )
        #   a.y_i = numpy.array( yt )
        a.x_i = numpy.array( yt )

        a.get_sweep_dirn()
        a.field_invert()
        amplitude_i,A = a.take_fft()

        # test data 
        # x_i = numpy.arange(4.0,8.0,0.01)
        # y_i = numpy.sin(2.0*pi*x) + numpy.sin(5.0*2.0*pi*x)  
        # A = fft.fft(y_i,pow(2,12) ) 
        F = -numpy.arange(0,len(A))/( (a.B_i[len(a.B_i)-1] - a.B_i[0])/len(a.B_i)*pow(2,12) )

        c1 = 982.0
        c2 = a.freq_i[len(A)-1] - c1 
        width = 270.0
        width6 = pow(width,6)
        filter = numpy.exp( -numpy.power(a.freq_i - c1,6)/width6) + numpy.exp( - numpy.power(a.freq_i-c2,6)/width6) 
   
        A1 = filter*A

#   for i in range(0,len(A)):
#      print a.freq_i[i],filter[i],sqrt( pow(A1[i].real,2) + pow(A1[i].imag,2))

        y2_i = fft.ifft(A1)   
   
        tmpx1_i = 1.0/a.IB_i
        tmpy1_i = y2_i.real
        tmpy_i = numpy.take( tmpy1_i, numpy.argsort(tmpx1_i) )
        tmpx_i = numpy.sort(tmpx1_i)
        dx = tmpx_i[1] - tmpx_i[0] - .000001
        x3_i,y3_i = dhva_routines.even_interpolate(tmpx_i,tmpy_i,tmpx_i[0],tmpx_i[-1],dx)

  
        outfile = open("./"+name[0:-3]+"flt","w")
        h = 0.0125   # modulation field in teslas
        bessarg = 2.0*pi*h*1.1e3
        for i in range(0,len(x3_i)):
            ibess = abs( 1.0/besselj( 2, bessarg/pow(x3_i[i],2) ) )
            if ibess>10.0:
                ibess = 10.0    # this to avoid infinities; it's rather awkward, to be sure
            y3_i[i] *= ibess
            outstr = str(x3_i[i]) + " " + str(y3_i[i])  + '\n'
            outfile.write(outstr)
# 
# # now do the rectification and low pass filtering:
# 
        a.B_i = numpy.array( x3_i )
        tmp_i = numpy.absolute( y3_i )
        offset = numpy.average( tmp_i)
        a.x_i = tmp_i - offset
        a.get_sweep_dirn()
        a.field_invert()
        amplitude_i,A = a.take_fft()
        width = 800 
        width2 = width*width
        filter = numpy.exp( -numpy.power(a.freq_i,2)/width2) + numpy.exp( -numpy.power(a.freq_i - (len(A)-1),2)/width2)
        A1 = filter*A
        y2_i = fft.ifft(A1)
        tmpx1_i = 1.0/a.IB_i
        tmpy1_i = y2_i.real
        tmpy_i = numpy.take( tmpy1_i, numpy.argsort(tmpx1_i) )
        tmpx_i = numpy.sort(tmpx1_i)
        dx = tmpx_i[1] - tmpx_i[0] - .000001
        x3_i,y3_i = dhva_routines.even_interpolate(tmpx_i,tmpy_i,tmpx_i[0],tmpx_i[-1],dx)
   
   
        outfile = open("./"+name[0:-3]+"lpf","w")
        for i in range(0,len(x3_i)):
            outstr = str(x3_i[i]) + " " + str(y3_i[i] + offset/1.8)  + '\n'
            outfile.write(outstr) 
# 
        infile.close()
        outfile.close()
