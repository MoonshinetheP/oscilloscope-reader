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

Filename:           plot.py

===================================================================================================

Description:

 

===================================================================================================

How to use this file:
    


===================================================================================================

Note:



===================================================================================================
'''

import sys
import os
from errno import EEXIST
import time

import numpy as np
import matplotlib.pyplot as plt

import waveforms as wf
import simulations as sim

class Plotter:

    def __init__(self, shape, instance, display = True, save = True):

        self.shape = shape
        self.instance = instance
        self.display = display
        self.save = save


        '''PLOT GENERATION'''
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12, 5))
        left, = ax1.plot(self.shape.tWF, self.shape.EWF, linewidth = 1, linestyle = '-', color = 'blue', marker = None, label = None, visible = True)
        right, = ax2.plot(self.instance.EPLOT, self.instance.i[:self.instance.EPLOT.size], linewidth = 1, linestyle = '-', color = 'red', marker = None, label = None, visible = True)
        

        '''PLOT SETTINGS'''
        ax1.set_xlim(np.amin(self.shape.tWF) - (0.1 * (np.amax(self.shape.tWF) - np.amin(self.shape.tWF))), np.amax(self.shape.tWF) + (0.1 * (np.amax(self.shape.tWF) - np.amin(self.shape.tWF))))
        ax1.set_ylim(np.amin(self.shape.EWF) - (0.1 * (np.amax(self.shape.EWF) - np.amin(self.shape.EWF))), np.amax(self.shape.EWF) + (0.1 * (np.amax(self.shape.EWF) - np.amin(self.shape.EWF))))
        ax1.set_title('E vs. t', pad = 15, fontsize = 20)
        ax1.set_xlabel('t / s', labelpad = 5, fontsize = 15)
        ax1.set_ylabel('E / V', labelpad = 5, fontsize = 15)

        ax2.set_xlim(np.amin(self.instance.EPLOT) - (0.1 * (np.amax(self.instance.EPLOT) - np.amin(self.instance.EPLOT))), np.amax(self.instance.EPLOT) + (0.1 * (np.amax(self.instance.EPLOT) - np.amin(self.instance.EPLOT))))
        ax2.set_ylim(np.amin(self.instance.i) - (0.1 * (np.amax(self.instance.i) - np.amin(self.instance.i))), np.amax(self.instance.i) + (0.1 * (np.amax(self.instance.i) - np.amin(self.instance.i))))
        ax2.set_title('i vs. E', pad = 15, fontsize = 20)
        ax2.set_xlabel('E / V', labelpad = 5, fontsize = 15)
        ax2.set_ylabel('i / A', labelpad = 5, fontsize = 15)

        if self.display == True:
            plt.show()

        plt.close()


"""
===================================================================================================
PLOTTING DATA FROM MAIN
===================================================================================================
"""

if __name__ == '__main__': 
        
     
    '''1. MAKE THE /DATA AND /PLOT FOLDERS''' 
    cwd = os.getcwd()

    try:
        os.makedirs(cwd + '/data')
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(cwd + '/data'):
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

    '''3. DESCRIBE THE WAVEFORM'''
    shape = wf.CV(Eini = 0, Eupp = 0.5, Elow = 0, dE = 0.01, sr = 0.05, ns = 1)
    #shape = wf.CSV(Eini = 0, Eupp = 0.5, Elow = 0, dE = 0.01, sr = 0.1, ns = 1, st = 0.0001, detailed = True, sampled = True, alpha = 0.25)
    
    '''4. RUN THE SIMULATION'''
    instance = sim.Capacitance(input = shape, Cd = 0.0001, Ru = 750)
    
    '''5. PLOT THE RESULTS'''
    plotted = Plotter(shape, instance)

    '''6. DEFINE THE END TIME'''
    end = time.time()

    print(f'The simulation took {end-start} seconds to plot')