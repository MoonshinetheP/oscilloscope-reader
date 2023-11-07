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

Filename:           operations.py

===================================================================================================

Description:

This file contains the code used by the oscilloscope-reader package to analyse oscilloscope data,
both simulated and imported. On its own, it will work out the position of the vertex potentials
from the oscilloscope data and update the potential waveform accordingly. Returned data can be in
its raw format, the result of a moving average operation, or the result of a current sampling
routine.

===================================================================================================

How to use this file:
    
This file has no standalone operational capabilities.

===================================================================================================

Note:

The functions for analysing the data are relatively simple, but the function for calculating the
position of the vertex potentials is a little more complicated. Currently, the programme works by
finding the highest point of each transient (i.e. the start), which works very well for simulated
data, but not as well for imported data, since the maximum point is not guaranteed to be the first
point of each transient and the rise of the transient itself is often comprised of several 
hundred data points. It does a good enough job for finding the vertex potentials, but is not as
efficient when it comes to current sampling between the peaks. Moving average analysis is not 
affected.

===================================================================================================
'''


import sys
import numpy as np


class Operations:

    '''Analyses the given data and uses it to format the given potential waveform \n

    Requires: \n
    shape - an instance of one of the potential waveform classes from the waveforms.py file\n
    data - an instance of either the Capacitance class from the simulations.py file or the Oscilloscope class from the fileopener.py file\n
    MA - a True or False option for whether moving average analysis is performed \n
    window - the window used for moving average anaysis \n
    step - the steps taken in moving average analysis \n 
    CS - a True or False option for whether current sampling analysis is performed \n
    alpha - the fraction of the step interval (from the end) which is averaged during current sampling analysis'''
    
    def __init__(self, shape, data, MA = False, window = 1000, step = 100, CS = False, alpha = 0.5):
        self.shape = shape
        self.data = data
        self.interval = shape.interval
        self.MA = MA
        self.window = window
        self.step = step
        self.CS = CS
        self.alpha = alpha

        '''DATA TYPE ERRORS'''
        if isinstance(self.MA, (bool)) is False:
            print('\n' + '' + '\n')
            sys.exit()
        if isinstance(self.window, (int)) is False:
            print('\n' + '' + '\n')
            sys.exit()
        if isinstance(self.step, (int)) is False:
            print('\n' + '' + '\n')
            sys.exit()
        if isinstance(self.CS, (bool)) is False:
            print('\n' + '' + '\n')
            sys.exit()
        if isinstance(self.alpha, (float, int)) is False:
            print('\n' + '' + '\n')
            sys.exit()

        if shape.type == 'linear' and data.label == 'simulated':
            self.E = self.shape.E
        else:
            self.Intervals()

        if self.MA == False and self.CS == False:
            self.Raw()
        if self.MA == True and self.CS == False:
            self.MovingAverage()
        if self.MA == False and self.CS == True:
            self.CurrentSampling()
        if self.MA == True and self.CS == True:
            print('\n' + 'Both analysis methods have been selected. Please choose either one or neither in order to get the raw data' + '\n')
            sys.exit()


    def Intervals(self):
        '''Finds intervals'''
        
        ix = 0
        self.peaks = np.array([])

        while ix < (self.data.i.size - self.interval + 1):
            self.peaks = np.append(self.peaks, np.argmax(np.abs(self.data.i[ix : ix + self.interval])) + ix + 1)
            ix += self.interval
        
        self.values =np.array([])
        for iy in self.peaks:
            self.values = np.append(self.values, self.data.i[int(iy)])

        iz = 0
        spacing = np.diff(self.values)
        for iz in spacing:
            if iz >= np.abs(self.values[1]):
                self.lv = int(self.peaks[np.where(spacing == iz)[0][0] + 1])
                if self.shape.dE > 0:
                        self.E = np.concatenate((self.shape.E[self.shape.udp + self.shape.dp - self.lv: ], self.shape.E[:self.shape.udp + self.shape.dp -self.lv]))
                elif self.shape.dE <0:
                         self.E = np.concatenate((self.shape.E[self.shape.ldp - self.lv: ], self.shape.E[:self.shape.ldp - self.lv]))
                break

            elif iz <= -np.abs(self.values[1]):
                self.uv = int(self.peaks[np.where(spacing == iz)[0][0]] + 1)
                if self.shape.dE > 0:
                        self.E = np.concatenate((self.shape.E[self.shape.udp - self.uv: ], self.shape.E[:self.shape.udp - self.uv]))
                elif self.shape.dE <0:
                         self.E = np.concatenate((self.shape.E[self.shape.dp + self.shape.ldp - self.uv: ], self.shape.E[:self.shape.dp + self.shape.ldp - self.uv]))
                break                         

        return (self.peaks, self.E)
    

    def Raw(self):
        '''Currently returns the oscilloscope data in its raw form'''
        self.method = 'no formatting'
            
        self.index = self.shape.index
        self.E = self.E
        self.i = self.data.i[:self.E.size + 1]


    def MovingAverage(self):
        '''Returns the moving average of the oscilloscope data in the form of voltage (detailed) vs. averaged current''' 
        self.method = f'a moving average using a {self.window} window and {self.step} steps'
        a = 0
        self.i = np.array([])
        while a < self.data.i.size - self.window + 1:
            self.i = np.append(self.i, np.average(self.data.i[a : a + self.window]))
            a += self.step

        self.index = self.shape.index
        self.E = self.E[::self.step]
        self.i = self.i[:self.E.size]
        

    def CurrentSampling(self):
        '''Returns the current average of each potential step in the oscilloscope data in the form of voltage (simplified) vs. averaged current'''
        self.method = f'current sampling using an alpha of {self.alpha}'

        self.i = np.array([])
        for ix in self.Intervals()[0]:
            try:
                data = self.data.i[int(ix) : int(ix + 1)]
            except:
                data = self.data.i[int(ix):] 
            period = self.alpha*(data.size)                                                    
            sampled = np.average(data[-int(period):])   
            self.i = np.append(self.i, sampled)
        
        self.index = self.shape.index
        self.E = self.E[::self.shape.interval]
        self.i = self.i
        
    
    def output(self):
        zipped = zip(self.index, self.E, self.i)
        return zipped