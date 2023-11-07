'''
===================================================================================================
Copyright (C) 2023 Steven Linfield

This file is part of the oscilloscope-reader package. This package is free software: you can 
redistribute it and/or modify it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or (at your option) any later 
version. This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
GNU General Public License for more details. You should have received a copy of the GNU General 
Public License along with oscilloscope-reader. If not, see https://www.gnu.org/licenses/
===================================================================================================

Package title:      oscilloscope-reader
Repository:         https://github.com/MoonshinetheP/oscilloscope-reader
Date of creation:   22/10/2022
Main author:        Steven Linfield (MoonshinetheP)
Collaborators:      None
Acknowledgements:   None

Filename:           reader.py

===================================================================================================

Description: 
This is the main file of the oscilloscope-reader package. All other files can be operated from 
here, although if it is necessary, many of the files can be operated individually from main.
 
===================================================================================================

How to use this file:
    
    1. Scroll down to the third point and choose the waveform you want to use, commenting out the 
       other waveform
    2. Edit the parameters of this waveform, keeping the following rules in mind
        a) If you want a scan going in the negative direction, use a negative dE value. 
        b) Negative dE values cannot be used when the start potential is the lower vertex potential
        c) Positive dE values cannot be used when the start potential is the upper vertex potential
        d) An oscilloscope sampling frequency (osf) of None gives a data point for each dE value
        e) Increasing the osf will increase the number of data points for each dE
        f) The osf cannot be set below the natural sampling frequency (given by sr/dE)
        h) If analysing imported oscilloscope data, use the osf of the oscilloscope
    3. Scroll down to the fourth point and choose the type of data you want to analyse, commenting
       out the other type
    4. If using imported data, make sure to include the conversion factor of V-to-A for the
       potentiostat/settings the data was recorded under
    5. If using simulations, choose the time constant parameters you want for the generated data
    6. Scroll down to the fifth point and choose the type of analysis you want to perform, keeping
       the following rules in mind:
       a) If both MA and CS are set to false, the raw data file will be returned
       b) If both MA and CS are set to true, no analysis will be performed
       c) Small steps can result in longer analysis times, but better resolution
       d) If the window is set larger than the number of data points per interval, it can cause 
          distortion, whilst lower window values will leave some transient features
    7. Scroll down to the sixth point and choose whether you want to display and/or save plots of 
       the analysed data
    8. Run the python file

The potential waveform data will be saved in a .txt file in the /data folder of the current working
directory, whilst the analysed oscilloscope data will be saved in a .txt file in the /analysis 
folder of the current working directory. If saved, the plotted data will be saved in a .png file in
the /plots folder of the current working drectory.

===================================================================================================
'''


import os
import time
from errno import EEXIST
from tkinter import filedialog
import fileopener as fo
import waveforms as wf
import simulations as sim
import operations as op
import plot as plt


'''1. MAKE THE /DATA, /ANALYSIS, & /PLOTS FOLDERS''' 
cwd = os.getcwd()

try:
    os.makedirs(cwd + '/data')
except OSError as exc:
    if exc.errno == EEXIST and os.path.isdir(cwd + '/data'):
        pass
    else: 
        raise

try:
    os.makedirs(cwd + '/analysis')
except OSError as exc:
    if exc.errno == EEXIST and os.path.isdir(cwd + '/analysis'):
        pass
    else: 
        raise

try:
    os.makedirs(cwd + '/plots')
except OSError as exc:
    if exc.errno == EEXIST and os.path.isdir(cwd + '/plots'):
        pass
    else: 
        raise

'''2. DEFINE THE START TIME'''
start = time.time()  

'''3. DESCRIBE THE WAVEFORM THAT WAS USED IN THE EXPERIMENT OR IS TO BE USED IN THE SIMULATION'''
#shape = wf.CyclicLinearVoltammetry(Eini = -0.3, Eupp = 0.85, Elow = -0.65, dE = -0.002, sr = 0.5, ns = 2, osf = 2000000)
shape = wf.CyclicStaircaseVoltammetry(Eini = -0.3, Eupp = 0.85, Elow = -0.65, dE = 0.002, sr = 0.5, ns = 1, osf = 2000000)

'''4. EITHER OPEN A REAL DATA FILE OR A SIMULATED DATA FILE'''
#data = fo.Oscilloscope(filedialog.askopenfilename(), cf = 0.000012)
data = sim.Capacitance(shape, Cd = 0.000050, Ru = 500)

'''5. PERFORM ANALYSIS ON THE DATA FILE'''
analysis = op.Operations(shape, data, MA = True, window = 50000, step = 1000, CS = False, alpha = 0.9)

'''6. VISUALISE THE ANALYSIS'''
plt.Plotter(shape, analysis, display = False, save = True)

'''7. SAVE THE DATA'''
with open(f'{cwd}/data/{time.strftime("%Y-%m-%d %H-%M-%S")} {shape.label}.txt', 'w') as file:
    for ix, iy, iz in shape.output():
        file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')

with open(f'{cwd}/analysis/{time.strftime("%Y-%m-%d %H-%M-%S")} {input.type} {shape.label} data with {analysis.method}.txt', 'w') as file:
    for ix, iy, iz in analysis.output():
        file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')
        
'''8. DEFINE THE END TIME'''
end = time.time()
print(f'The oscilloscope file took {end-start} seconds to analyse')