'''
Created on Apr 13, 2011

@author: asutton
'''

import return_DataToPlot as DP
import analysis_sub as asub
# import netCDF4 as netCDF4
# from pylab import *
import convert_CDF as cnv
import os
# import numpy as np
import printresults as pr
from yesno import query_yes_no
import matplotlib.pyplot as plt

# Check OS
check_os = os.name

# Select file to work on
# *NIX Path format
if (check_os == 'posix'):
    path = '/home/asutton/Dropbox/School/Current/YbRh2Si2/Raw_Data/February_2012/'
    outpath = path
    progpath = '/home/asutton/Dropbox/workspace/dhva_edit/src/'

# Windows path format
elif (check_os == 'nt'):
    path = 'E:\Google Drive\Data Sync\Dropbox\workspace\dhva_analyzer\src'
    outpath = path
    progpath = 'E:\Google Drive\Data Sync\Dropbox\workspace\dhva_edit\src'

name = '2012_02_22_02_YbRh2Si2_000.nc'

# Convert all files in the directory from netCDF to .dat
convert = 0
if convert:
    cnv.convert_CDF(path)

# initialize figure counter
figure_counter = 0

# Get variables to plot
plotvariables, nc = DP.return_DataToPlot(path, name)
os.chdir(progpath)

# Analyze?
a_vars = dict()
Analyze_A = 1
a_vars['Sample'] = 'A'
# Which harmonic?
a_vars['Harmonic'] = '1'
# Range?
a_vars['min_field'] = 14
a_vars['max_field'] = 16
# Analyze the lock-in Y data?
a_vars['Y'] = 1
# Despike the data?
a_vars['despike'] = 1
# Which mother wavelet?
a_vars['mother'] = 'coif2'
# How many levels of decomposition?
a_vars['wavelet_lvls'] = 2
# Smooth?
a_vars['smoothdat'] = 0
# Smoothing type
a_vars['smoothtype'] = 'hamming'
# Window?
a_vars['window'] = 1
# Which kind of window?
a_vars['windowtype'] = 'hamming'
# Write the data to a file?
a_vars['write'] = 0
a_vars['write_fft'] = 0

# Analyze B?
b_vars = dict()
Analyze_B = 0
b_vars['Sample'] = 'B'
b_vars['Harmonic'] = '1'
b_vars['min_field'] = 14
b_vars['max_field'] = 16
b_vars['Y'] = 1
b_vars['despike'] = 0
b_vars['mother'] = 'coif2'
b_vars['wavelet_lvls'] = 2
b_vars['smoothdat'] = 0
b_vars['smoothtype'] = 'hamming'
b_vars['window'] = 1
b_vars['windowtype'] = 'hamming'
b_vars['write'] = 0
b_vars['write_fft'] = 0

# Analyze C?
c_vars = dict()
Analyze_C = 0
c_vars['Sample'] = 'C'
c_vars['Harmonic'] = '2'
c_vars['min_field'] = 14.1
c_vars['max_field'] = 16
c_vars['Y'] = 1
c_vars['despike'] = 1
c_vars['mother'] = 'coif2'
c_vars['wavelet_lvls'] = 2
c_vars['smoothdat'] = 0
c_vars['smoothtype'] = 'hamming'
c_vars['window'] = 0
c_vars['windowtype'] = 'hanning'
c_vars['write'] = 0
c_vars['write_fft'] = 0

# Analyze Raw Channels E & F?
e_vars = dict()
Analyze_Nolock = 0
e_vars['Sample'] = 'E'
e_vars['Harmonic'] = '0'
e_vars['min_field'] = 14.1
e_vars['max_field'] = 16
e_vars['Y'] = 0
e_vars['despike'] = 1
e_vars['mother'] = 'coif2'
e_vars['wavelet_lvls'] = 2
e_vars['smoothdat'] = 0
e_vars['smoothtype'] = 'hamming'
e_vars['window'] = 0
e_vars['windowtype'] = 'hanning'
e_vars['write'] = 0
e_vars['write_fft'] = 0


if Analyze_A:
    figure_counter += 1
    a_analyzed = asub.analysis_sub(name, path, plotvariables, figure_counter, **a_vars)
    pr.print_results(a_analyzed, a_vars)
    # print('A is done')

if Analyze_B:
    figure_counter += 1
    b_analyzed = asub.analysis_sub(name, path, plotvariables, figure_counter, **b_vars)
    pr.print_results(b_analyzed, b_vars)

if Analyze_C:
    figure_counter += 1
    c_analyzed = asub.analysis_sub(name, path, plotvariables, figure_counter, **c_vars)
    pr.print_results(c_analyzed, c_vars)

if Analyze_Nolock:
    figure_counter += 1
    e_analyzed = asub.analysis_sub(name, path, plotvariables, figure_counter, **e_vars)
    pr.print_results(e_analyzed, e_vars)

keep_plots = query_yes_no("Do you wish to keep the plot windows open?")

if keep_plots == 'no':
    plt.close('all')

nc.close
os.chdir(progpath)
# print('all done')
# show()
