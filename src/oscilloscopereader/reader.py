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
    


===================================================================================================

Note:



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
#shape = wf.CyclicLinearVoltammetry(Eini = -0.3, Eupp = 0.85, Elow = -0.65, dE = 0.002, sr = 0.5, ns = 2, osf = 2000000)
shape = wf.CyclicStaircaseVoltammetry(Eini = -0.65, Eupp = 0.85, Elow = -0.65, dE = 0.005, sr = 0.5, ns = 1, osf = 20000)

'''4. EITHER OPEN A REAL DATA FILE OR A SIMULATED DATA FILE'''
#input = fo.Oscilloscope(filedialog.askopenfilename(), cf = 0.000012)
input = sim.Capacitance(input = shape, Cd = 0.000050, Ru = 500)

'''5. PERFORM ANALYSIS ON THE DATA FILE'''
instance = op.Operations(shape, input, MA = False, window = 50000, step = 1000, CS = False, alpha = 0.9)

'''6. VISUALISE THE ANALYSIS'''
plt.Plotter(shape, instance, display = True, save = True)

'''7. SAVE THE DATA'''
with open(f'{cwd}/data/{time.strftime("%Y-%m-%d %H-%M-%S")} {shape.label}.txt', 'w') as file:
    for ix, iy, iz in shape.output():
        file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')

with open(f'{cwd}/analysis/{time.strftime("%Y-%m-%d %H-%M-%S")} {input.type} {shape.label} data with {instance.analysis}.txt', 'w') as file:
    for ix, iy, iz in instance.output():
        file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')
        
'''8. DEFINE THE END TIME'''
end = time.time()
print(f'The oscilloscope file took {end-start} seconds to analyse')