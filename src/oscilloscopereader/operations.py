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

 

===================================================================================================

How to use this file:
    


===================================================================================================

Note:



===================================================================================================
'''


import sys
import os
import time
import numpy as np
from tkinter import filedialog
import waveforms as wf
import simulations as sim
import fileopener as fo

from errno import EEXIST


class Operations:
    def __init__(self, shape, input, MA = False, window = 1000, step = 100, CS = False, alpha = 0.5):
        self.shape = shape
        self.input = input.i
        self.interval = shape.interval
        self.cf = input.cf
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

        while ix < (self.input.size - self.interval + 1):
            self.peaks = np.append(self.peaks, np.argmax(np.abs(self.input[ix : ix + self.interval])) + ix + 1)
            ix += self.interval
        
        self.values =np.array([])
        for iy in self.peaks:
            self.values = np.append(self.values, self.input[int(iy)])

        iw = 0
        self.troughs = np.array([])
        while iw < self.peaks.size:
            self.troughs = np.append(self.troughs, self.peaks[iw] - np.argmin(self.input[int(self.peaks[iw]) - 200: int(self.peaks[iw])]))
            iw += 1

        iz = 0
        spacing = np.diff(self.values)
        for iz in spacing:
            if iz <= -np.abs(self.values[1]):
                self.lv = int(self.troughs[np.where(spacing == iz)[0][0]])
                if self.shape.dE > 0:
                        self.EPLOT = np.concatenate((self.shape.EPLOT[self.shape.uppdp + self.shape.dp - self.lv: ], self.shape.EPLOT[:self.shape.uppdp + self.shape.dp -self.lv]))
                elif self.shape.dE <0:
                         self.EPLOT = np.concatenate((self.shape.EPLOT[self.shape.lowdp - self.lv: ], self.shape.EPLOT[:self.shape.lowdp - self.lv]))
                break

            elif iz >= np.abs(self.values[1]):
                self.uv = int(self.troughs[np.where(spacing == iz)[0][0]])
                if self.shape.dE > 0:
                        self.EPLOT = np.concatenate((self.shape.EPLOT[self.shape.uppdp - self.uv: ], self.shape.EPLOT[:self.shape.uppdp - self.uv]))
                elif self.shape.dE <0:
                         self.EPLOT = np.concatenate((self.shape.EPLOT[self.shape.dp + self.shape.lowdp - self.uv: ], self.shape.EPLOT[:self.shape.dp + self.shape.lowdp - self.uv]))
                break                         

        return (self.peaks, self.troughs, self.EPLOT)
    

    def Raw(self):
        '''Currently returns the oscilloscope data in its raw form'''
        self.analysis = 'no formatting'
            
        self.index = self.shape.index
        self.EPLOT = self.EPLOT
        self.i = self.input * -self.cf


    def MovingAverage(self):
        '''Returns the moving average of the oscilloscope data in the form of voltage (detailed) vs. averaged current''' 
        self.analysis = f'a moving average using a {self.window} window and {self.step} steps'
        a = 0
        self.i = np.array([])
        while a < self.input.size - self.window + 1:
            self.i = np.append(self.i, np.average(self.input[a : a + self.window]))
            a += self.step

        self.index = self.shape.index
        self.EPLOT = self.EPLOT[::self.step]
        self.i = self.i * -self.cf
        


    def CurrentSampling(self):
        '''Returns the current average of each potential step in the oscilloscope data in the form of voltage (simplified) vs. averaged current'''
        self.analysis = f'current sampling using an alpha of {self.alpha}'

        self.i = np.array([])
        for ix in self.Intervals()[0]:
            try:
                data = self.input[int(ix) : int(ix + 1)]
            except:
                data = self.input[int(ix):] 
            period = self.alpha*(data.size)                                                    
            sampled = np.average(data[-int(period):])   
            self.i = np.append(self.i, sampled)
        
        self.index = self.shape.index
        self.EPLOT = self.EPLOT[::self.shape.interval]
        self.i = self.i * -self.cf
        
    
    def output(self):
        zipped = zip(self.index, self.EPLOT, self.i)
        return zipped


if __name__ == '__main__':
    
    '''1. MAKE A /ANALYSIS FOLDER''' 
    cwd = os.getcwd()

    try:
        os.makedirs(cwd + '/analysis')
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(cwd + '/analysis'):
            pass
        else: 
            raise

    '''2. DEFINE THE START TIME'''
    start = time.time()  

    '''3. ANALYSE THE DEFINED FILE OR SIMULATION'''
    shape = wf.CyclicLinearVoltammetry(Eini = -0.3, Eupp = 0.8, Elow = -0.65, dE = 0.002, sr = 0.5, ns = 1, osf = 2000000)
    
    input = fo.Oscilloscope(filedialog.askopenfilename(), cf = 0.000012)
    #input = sim.Capacitance(input = shape, Cd = 0.000050, Ru = 500)
    
    instance = Operations(shape, input, MA = True, window = 20000, step = 1000, CS = False, alpha = 0.9)

    '''4. SAVE THE DATA'''
    filepath = f'{cwd}/analysis/{time.strftime("%Y-%m-%d %H-%M-%S")} {instance.analysis}.txt'
    with open(filepath, 'w') as file:
        for ix, iy, iz in instance.output():
            file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')

    '''5. DEFINE THE END TIME'''
    end = time.time()
    print(f'The oscilloscope file took {end-start} seconds to analyse')