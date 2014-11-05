'''
Created on Feb 24, 2012

@author: asutton
'''
# import netCDF4 as netCDF4
# from pylab import *
# from scipy.optimize import leastsq
from scipy import signal
import numpy as np
import fit_bg
# import smooth
import sortarray as sa
# import convert_CDF as cnv
# import return_DataToPlot as DP
# from sys import exit
from dhva_routines import next_pow_2
from wavelet_filter import wavelet_filter as wf
import interp_field as i_f
from take_fft import take_fft
import select_data
import find_angle as fa
import peakfind as pf
import os
import matplotlib.pyplot as plt
# from matplotlib import pyplot
# from matplotlib import figure

def analysis_sub(name, path, plotvariables, figure_counter_sub, Sample, Harmonic, min_field, max_field, Y, despike, mother, wavelet_lvls, smooth, smoothtype, window, windowtype, write, write_fft):

    # figure_counter_sub = figure_counter + 1
    UnSortCurrentH_in = plotvariables['B']
    if Sample == 'E':
        x_in = plotvariables['E']
        y_in = plotvariables['F']
    else:
        data_to_use_x = Sample + Harmonic + 'X'
        data_to_use_y = Sample + Harmonic + 'Y'
        x_in = plotvariables[data_to_use_x]
        y_in = plotvariables[data_to_use_y]

    x_units = UnSortCurrentH_in.units
    y_units = x_in.units

    UnSortCurrentH, x, y = select_data.select_data(UnSortCurrentH_in, x_in, y_in, min_field, max_field)

    power = next_pow_2(len(UnSortCurrentH))
    SampleRate = len(UnSortCurrentH[:])/(np.max(UnSortCurrentH[:]) - np.min(UnSortCurrentH[:]))

    # Determine the best phase angle to use from Dan's method and combine X & Y components using this value
    UnSortSignal,UnSortSignalY = fa.find_angle(x,y)

    # Sort the x & y values in descending order of x
    CurrentH, Signal = sa.sortarray(UnSortCurrentH[:], UnSortSignal,0)

    # Fit polynomial background to data
    fitdata = fit_bg.bg_polynomial(CurrentH, Signal, 3)

    # despike the data
    # despike = 1
    if despike:
        despiked_data = fitdata[0]
        # despiked_data = wf(despiked_data,2,'haar')
        despiked_data = wf(despiked_data, wavelet_lvls, mother)
        # despiked_data = wf(despiked_data,1, 'sym2')
    else:
        despiked_data = fitdata[0]

    # Run field inverter/interpolator
    interp_data, rebinH, invDeltaH = i_f.inv_field(despiked_data, CurrentH)
    newH = 1/rebinH
    #window the data

    if smooth:
        smoothed_data = smooth.smooth(interp_data, 30, smoothtype)
    else:
        smoothed_data = interp_data

    if window:
        window_func = eval('signal.'+windowtype)
        window_to_use = window_func(len(smoothed_data))
        windowed_data = window_to_use*smoothed_data
    else:
        windowed_data = smoothed_data

    DeltaFreq = 1/(invDeltaH)

    # Pad data with zeros for FFT
    pad_mult = 10
    zero_matrix = np.zeros(len(windowed_data)*pad_mult/2)
    pad_wind_data = np.append(windowed_data, zero_matrix)
    # pad_wind_data = np.append(zero_matrix, pad_wind_data)

    Freq, FFT_Signal = take_fft(pad_wind_data, 17, DeltaFreq)

    # AnalyzeY = 0
    if Y:
        # Sort the x & y values in descending order of x
        CurrentHY, SignalY = sa.sortarray(UnSortCurrentH[:], UnSortSignalY, 0)

        # Fit polynomial background to data
        fitdataY = fit_bg.bg_polynomial(CurrentHY, SignalY, 3)

        # despike the data
        # despike = 1
        if despike:
            despiked_dataY = fitdataY[0]
        # despiked_data = wf(despiked_data,2,'haar')
            despiked_dataY = wf(despiked_dataY, wavelet_lvls, mother)
        # despiked_data = wf(despiked_data,1, 'sym2')
        else:
            despiked_data = fitdata[0]

    # Run field inverter/interpolator
        interp_dataY, rebinHY, invDeltaHY = i_f.inv_field(despiked_dataY, CurrentHY)
        newHY = 1/rebinHY
    # window the data

        if smooth:
            smoothed_dataY = smooth.smooth(interp_dataY, 30, smoothtype)
        else:
            smoothed_dataY = interp_dataY

        if window:
            window_func = eval('signal.'+windowtype)
            window_to_use = window_func(len(smoothed_dataY))
            windowed_dataY = window_to_use*smoothed_dataY
        else:
            windowed_dataY = smoothed_dataY

        DeltaFreqY = 1/(invDeltaHY)

        # Pad data with zeros for FFT
        pad_mult = 10
        zero_matrixY = np.zeros(len(windowed_dataY)*pad_mult/2)
        pad_wind_dataY = np.append(windowed_dataY, zero_matrixY)
        # pad_wind_data = np.append(zero_matrix, pad_wind_data)

        FreqY, FFT_SignalY = take_fft(pad_wind_dataY, 17, DeltaFreqY)

    # Plot raw data
    sig_Plot = plt.figure(figure_counter_sub)
    plt.clf()
    sig_Plot.suptitle('Sample ' + Sample, fontsize=16, fontweight='bold')

    sig_raw = sig_Plot.add_subplot(221)
    sig_raw.set_title('Raw Data', fontsize=12)
    sig_raw.plot(UnSortCurrentH, x, 'r', label="in-phase X")
    sig_raw.plot(UnSortCurrentH, y, 'g', label="out-of-phase Y")
    sig_raw.set_xlabel('Field (' + x_units + ')', fontsize=12)
    sig_raw.set_ylabel('Signal (' + y_units + ')', fontsize=12)
    sig_raw.legend(loc=1)
    # Plot result
    sig_raw.plot(CurrentH, Signal, 'b')

    # Plot original data and polynomial fit through it
    sig_fit = sig_Plot.add_subplot(222)
    sig_fit.set_title('Background Fit', fontsize=12)
    sig_fit.plot(CurrentHY, SignalY, 'g')
    sig_fit.plot(CurrentHY, fitdataY[1], 'r')
    sig_fit.plot(CurrentHY, fitdataY[0], 'y')
    sig_fit.set_xlabel('Field (' + x_units + ')', fontsize=12)
    sig_fit.set_ylabel('Signal (' + y_units + ')', fontsize=12)

    # Plot Windowed data
    sig_windowed = sig_Plot.add_subplot(223)
    sig_windowed.set_title('Windowed Data', fontsize=12)
    sig_windowed.plot(rebinHY, windowed_dataY)
    # sig_windowed.plot(rebinH,window_to_use)
    sig_windowed.set_xlabel('Field (' + x_units + ')', fontsize=12)
    sig_windowed.set_ylabel('Signal (' + y_units + ')', fontsize=12)

    # Plot FFT
    sig_fft = sig_Plot.add_subplot(224)
    sig_fft.set_title('FFT', fontsize=12)
    sig_fft.plot(Freq, FFT_Signal, 'g')
    sig_fft.axis([0, 34000, 0, max(FFT_Signal) + 0.2*max(FFT_Signal)])
    sig_fft.set_xlabel('dHvA Frequency (' + x_units + ')', fontsize=12)
    sig_fft.set_ylabel('Amplitude', fontsize=12)
    if Y:
        sig_fft.plot(FreqY, FFT_SignalY, 'r')
    plt.draw()

    dHvApeaks = pf.peakfind(Freq, FFT_Signal, sig_fft)

    if (write == 1):
        os.chdir(path)
        filename = 'Sample_'+Sample+'_X.dat'
        file_exist = os.path.isfile(filename)
        # print(file_exist)
        if (file_exist):
            openfile = open(filename, 'a')
            outstr = name[0:-3] + '\t'
            for i in range(0, len(dHvApeaks)):
                outstr = outstr + '\t' + str(dHvApeaks[i][0]) + '\t' + str(dHvApeaks[i][1])
            openfile.write(outstr + '\n')
            openfile.close()
        else:
            openfile = open(filename, 'w')
            headerstring = "#This file is a list of peaks generated by Aaron's dHvA analysis program. The files listed below are found in the path " + path + '\n' + "#File , rotation file , F1 , A1 , F2 , A2 , ..." + '\n'
            outstr = name[0:-3] + '\t'
            for i in range(0, len(dHvApeaks)):
                outstr = outstr + '\t' + str(dHvApeaks[i][0]) + '\t' + str(dHvApeaks[i][1])
            openfile.write(headerstring + outstr + '\n')
            openfile.close()

    if (write_fft == 1):
        os.chdir(path)
        zipped = zip(Freq, FFT_Signal)
        # print zipped
        filename_fft = 'Sample_'+Sample+'_'+name[0:-3]+'_X_fft.dat'
        np.savetxt(filename_fft, zipped, delimiter='\t')
        # openfile_fft = open(filename_fft, 'w')
        # outstr_fft = Freq + '\t' FFT_Signal
        # openfile_fft.write(outstr)
        # openfile_fft.close()

    if Y:
        dHvApeaksY = pf.peakfind(FreqY,FFT_SignalY,sig_fft)

        if (write == 1):
            os.chdir(path)
            filenameY = 'Sample_' + Sample + '_Y.dat'
            file_existY = os.path.isfile(filenameY)
            # print(file_exist)
            if (file_existY):
                openfileY = open(filenameY, 'a')
                outstrY = name[0:-3] + '\t'
                for i in range(0, len(dHvApeaksY)):
                    outstrY = outstrY + '\t' + str(dHvApeaksY[i][0]) + '\t' + str(dHvApeaksY[i][1])
                openfileY.write(outstrY + '\n')
                openfileY.close()
            else:
                openfileY = open(filenameY, 'w')
                headerstringY = "#This file is a list of peaks generated by Aaron's dHvA analysis program. The files listed below are found in the path " + path + '\n' + "#File , rotation file , F1 , A1 , F2 , A2 , ..." + '\n'
                outstrY = name[0:-3] + '\t'
                for i in range(0, len(dHvApeaksY)):
                    outstrY = outstrY + '\t' + str(dHvApeaksY[i][0]) + '\t' + str(dHvApeaksY[i][1])
                openfileY.write(headerstringY + outstrY + '\n')
                openfileY.close()

        if (write_fft == 1):
            os.chdir(path)
            zippedY = zip(FreqY, FFT_SignalY)
            #print zipped
            filename_fftY = 'Sample_'+ Sample + '_' + name[0:-3] + '_Y_fft.dat'
            np.savetxt(filename_fftY, zippedY, delimiter='\t')
    else:
        dHvApeaksY = []
   # print(dHvApeaks)
   # print(len(dHvApeaks))
    peak_result = {'XPeaks':dHvApeaks,'YPeaks':dHvApeaksY}
    return peak_result
