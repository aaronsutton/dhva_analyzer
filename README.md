#Aaron's dHvA data analyzer

This is a python based analyzer for de Haas-van Alphen quantum oscillation measurements written as a selection of
python scripts. It is certainly a work in progress and is based upon Patrick Rourke's LabView dHvA analyzer. It is
designed to work specifically with the datasets created in our lab. 

##Requirements
* Python 2.7 (not tested with Python3)
* iPython
* Pywavelets package
* Numpy
* Scipy
* Matplotlib
* netCDF4/HDF5

##Usage
At present, the end user need only modify the variables found in dhva_main.py. These allow the user to select the data to be analyzed (Channels A,B,C,E,F), the harmonic to analyze on (1,2), and allows for a variety of options including background signal subtraction, smoothing, despiking, windowing, convert netCDF to dat, write results to file, etc.

After selecting the parameters, the user runs dhva_main.py from an iPython shelland is presented with a four paned plot
showing the data through the various stages of analysis. The bottom right plot can be clicked to select manually the
various dHvA peaks. The user click 3 times with the left mouse button, once on either side of the peak and once to
indicte the centroid. Points made in error can be removed one at a time by right clicking. The program then attempts to
fit a Gaussian to the peak. This process is repeated for each peak of interest. When finished, one clicks the mouse
wheel to stop the input. The resulting peaks are printed to the terminal in centroid, amplitude form and are written to
file (if selected). This process is repeated for both X and Y (lock-in channels) if desired, and for each sample
channel. Currently, phase optimization between X and Y is not implemented as it was found to be more useful to analyze
in X and Y separately.
