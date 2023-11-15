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

Filename:           waveforms.py

===================================================================================================

Description:

This file contains the code used by the oscilloscope-reader package to generate potential waveforms
which are then used in simulations.py to prepare simulated data and in operations.py and plot.py to 
accompany oscilloscope data. 

===================================================================================================

How to use this file:
    
Whilst this file is primarily used by other files, it can also be used on its own in order to 
prepare potential waveforms for data processing, educational purposes, other simulations, etc.

In order to use this file:
    1. Scroll down the the bottom of the file, to the 'GENERATING WAVEFORMS FROM MAIN' section.
    2. In the third point of this section, choose the waveform you want to generate, commenting out
       the other waveform
    3. Edit the parameters of this waveform, keeping the following rules in mind
        a) If you want a scan going in the negative direction, use a negative dE value. 
        b) Negative dE values cannot be used when the start potential is the lower vertex potential
        c) Positive dE values cannot be used when the start potential is the upper vertex potential
        d) An oscilloscope sampling frequency (osf) of None gives a data point for each dE value
        e) Increasing the osf will increase the number of data points for each dE
        f) The osf cannot be set below the natural sampling frequency (given by sr/dE)
    4. Run the python file

The potential waveform data will be saved in a .txt file in the /data folder of the current working
directory.

===================================================================================================

Notes:

The CyclicStaircaseVoltammetry class is a child of the CyclicLinearVoltammetry class. This was done 
because the waveform used in operations.py file is the same for both types of voltammetry (i.e. a 
linear triangular waveform with the same number of points as measured using an oscilloscope), since 
plotting vs. a staircase is not possible. The only difference for the child compared to the parent
is that the waveform exported for checking or plotting needs more preparation in order to show its 
true staircase form.

The CyclicLinearVoltammetry class is itself a child of the Waveforms class. This parent class
initialises all of the parameters used by the child and grandchild, checks the parameter types and
values, then calculates a few other parameters which are used by both children and also other files
such as simulations.py and operations.py. It also features the function for exporting the waveform
data from the main of this file.

When using the waveform classes in this file, bear in mind that increasing the oscilloscope
sampling frequency (i.e. the osf) increases the size of the waveform data and the time required to
generate the waveform. Since the osf is a fixed rate, selecting slower scan rates will naturally 
increase the number of points in the final waveform data. Keep this in mind, as it may be more
efficient to decrease the osf if you want waveform data for a slower scan rate (as you would do 
when using an oscilloscope). If the value of osf is changed to None, then only one point per dE (or
two in the case of CyclicStaircaseVoltammetry) will be generated, giving you the simplest possible
waveform.

===================================================================================================
'''


import sys
import os
import time
import numpy as np
from errno import EEXIST


class Waveform:

    '''Parent class for cyclic voltammetry waveforms \n
    Contains the parameter initialisation, error management, parameter calculations, and output function used by all child classes'''

    def __init__(self, Eini, Eupp, Elow, dE, sr, ns, osf):

        '''PARAMETER INITIALISATION'''
        self.Eini = Eini        # initial potential (in V)
        self.Eupp = Eupp        # upper vertex potential (in V)
        self.Elow = Elow        # lower vertex potential (in V)
        self.dE = dE        # step size (in V)
        self.sr = sr        # scan rate (in V/s)
        self.ns = ns        # number of scans
        self.osf = osf      # oscilloscope sampling frequency (in Sa/s)
        
        '''DATATYPE ERRORS'''
        if isinstance(self.Eini, (float, int)) is False:        # checks that the given initial potential is a float or an integer value
            print('\n' + 'An invalid datatype was used for the start potential. Enter either a float or an integer value corresponding to a potential in V.' + '\n')
            sys.exit()
        if isinstance(self.Eupp, (float, int)) is False:        # checks that the given upper vertex potential is a float or an integer value
            print('\n' + 'An invalid datatype was used for the upper vertex potential. Enter either a float or an integer value corresponding to a potential in V.' + '\n')
            sys.exit()        
        if isinstance(self.Elow, (float, int)) is False:        # checks that the given lower vertex potential is a float or an integer value
            print('\n' + 'An invalid datatype was used for the lower vertex potential. Enter either a float or an integer value corresponding to a potential in V.' + '\n')
            sys.exit()      
        if isinstance(self.dE, (float)) is False:       # checks that the given step size is a float value
            print('\n' + 'An invalid datatype was used for the step potential. Enter a float value corresponding to a potential in V.' + '\n')
            sys.exit()    
        if isinstance(self.sr, (float, int)) is False:      # checks that the given scan rate is a float or an integer value
            print('\n' + 'An invalid datatype was used for the scan rate. Enter a float or an integer value corresponding to the scan rate in V/s.' + '\n')
            sys.exit() 
        if isinstance(self.ns, (int)) is False:     # checks that the given number of scans is an integer value
            print('\n' + 'An invalid datatype was used for the number of scans. Enter an integer value corresponding to the scan rate in V/s.' + '\n')
            sys.exit() 
        if isinstance(self.osf, (int, type(None))) is False:        # checks that the given oscilloscope sampling frequency is an integer value or None
            print('\n' + 'An invalid datatype was used for the oscilloscope sampling rate. Enter an integer value or None.' + '\n')
            sys.exit()

        '''DATA VALUE ERRORS'''
        if self.Eupp == self.Elow:      # checks that the potential window is greater than 0
            print('\n' + 'Upper and lower vertex potentials must be different values' + '\n')
            sys.exit()
        if self.Eupp < self.Elow:       #checks that the upper vertex potential is more positive than the lower vertex potential
            print('\n' + 'Upper vertex potential must be greater than lower vertex potential' + '\n')
            sys.exit()  
        if self.Eini < self.Elow:       #checks that the initial potential is equal to or more positive than the lower vertex potential
            print('\n' + 'Start potential must be higher than or equal to the lower vertex potential' + '\n')
            sys.exit()
        if self.Eini > self.Eupp:       # checks that the initial potential is equal to or more negative than the upper vertex potential
            print('\n' + 'Start potential must be lower than or equal to the upper vertex potential' + '\n')
            sys.exit()
        if self.dE == 0:        # checks that step size is not zero        
            print('\n' + 'Step potential must be a non-zero value' + '\n')
            sys.exit()
        if abs(self.dE) > abs(self.Eupp - self.Elow):       # checks that the step size is not greater than the potential window
            print('\n' + 'Step potential must not be greater than the potential window' + '\n')
            sys.exit()
        if self.Eini == self.Elow and self.dE < 0:      # checks that the step size is not negative when going in an initial positive direction
            print('\n' + 'Step potential must be a positive value for a positive scan direction' + '\n')
            sys.exit()
        if self.Eini == self.Eupp and self.dE > 0:      # checks that the step size is not positive when going in an initial negative direction
            print('\n' + 'Step potential must be a negative value for a negative scan direction' + '\n')
            sys.exit()
        if self.sr <= 0:        # checks that the scan rate is not 0
            print('\n' + 'Scan rate must be a positive non-zero value' + '\n')
            sys.exit()
        if self.ns <=0:     #checks that the number of scans is 1 or more
            print('\n' + 'Number of scans must be a positive non-zero value' + '\n')
            sys.exit()
        if type(self.osf) == int and self.osf < round(np.abs(self.sr / self.dE)):       # checks that an integer osf value is above the natural sampling frequency
            print('\n' + 'Oscilloscope sampling frequency is set below the natural sampling rate. Set it to None or increase the frequency' + '\n')
            sys.exit() 

        '''PARAMETER DEFINITIONS'''
        if self.osf == None:
            self.osf = round(np.abs(self.sr / self.dE))     # sets the osf to the natural sampling frequency when osf is initially None

        self.interval = round(np.abs(self.dE / self.sr) * self.osf)     # number of sampling points between steps (Sa)

        self.window = round(self.Eupp - self.Elow, 3)       # potential window (in V) rounded to 3 d.p
        self.dp = round(self.window * round(self.osf / self.sr))       # number of data points per potential window (in Sa) rounded to 0 d.p
        self.uwindow = round(self.Eupp - self.Eini, 3)      # upper partial potential window (in V) rounded to 3 d.p
        self.udp = round(self.uwindow * round(self.osf / self.sr))       # number of data points per upper partial potential window (in Sa) rounded to 0 d.p
        self.lwindow = round(self.Eini - self.Elow, 3)      # lower partial potential window (in V) rounded to 3 d.p
        self.ldp = round(self.lwindow * round(self.osf / self.sr))       # number of data points per lower partial potential window (in Sa) rounded to 0 d.p
        
        self.tmax = round(2 * self.ns * self.window / self.sr, 6)       # end time for potential waveform (in s) rounded to 6 d.p
        self.dt = round((1 / self.osf), 9)      # interval time between data points (in s) rounded to 9 d.p

        self.steps = round(np.abs(self.window / self.dE))       # number of steps per potential window
        self.usteps = round(np.abs(self.uwindow / self.dE))     # number of steps per uppwer partial potential window
        self.lsteps = round(np.abs(self.lwindow / self.dE))     # number of steps per lower partial potential window


    def output(self):
        '''Returns the waveform for checking or data processing purposes'''
        
        zipped = zip(self.indexWF, self.tWF, self.EWF)      # zipped array containing waveform data
        return zipped



class CyclicLinearVoltammetry(Waveform):

    '''Creates the waveform for a cyclic linear voltammetry procedure \n
    Requires: \n
    Eini - initial potential (in V) \n
    Eupp - upper vertex potential (in V) \n
    Elow - lower vertex potential (in V) \n
    dE - step size (in V) \n
    sr - scan rate (in V/s) \n
    ns - number of scans \n
    osf - oscilloscope sampling frequency (in Sa/s)
    '''
    
    def __init__(self, Eini, Eupp, Elow, dE, sr, ns, osf):
        super().__init__(Eini, Eupp, Elow, dE, sr, ns, osf)     # adopts parameters from the Waveform parent class
        
        '''LABELS'''
        self.type = 'linear'        # label for use in simulations.py
        self.label = 'CV'       # label for file naming

        '''INDEX'''
        self.index = np.arange(0, round((self.tmax + self.dt) / self.dt), 1)        # produces a rounded indexing array which starts from 0
        
        '''TIME'''
        self.t = np.round(self.index * self.dt, 9)      # converts the indexing array into a time array (rounded to 9 d.p)

        '''POTENTIAL'''
        self.E = np.array([self.Eini])      # creates a potential array containing the initial potential
        
        '''STARTING FROM LOWER VERTEX POTENTIAL''' 
        if self.Eini == self.Elow:      # activates in cases where the initial potential is equal to the lower vertex potential                 
            for ix in range(0, self.ns):        # loops through the number of scans
                self.E = np.append(self.E, np.round(np.linspace(self.Eini + (self.window / self.dp), self.Eupp, self.dp, endpoint = True), 9))      # adds the positive scan direction portion of the potential window to the potential array (rounded to 9 d.p)
                self.E = np.append(self.E, np.round(np.linspace(self.Eupp - (self.window / self.dp), self.Eini, self.dp, endpoint = True), 9))      # adds the negtive scan direction portion of the potential window to the potential array (rounded to 9 d.p)

        '''STARTING FROM UPPER VERTEX POTENTIAL'''
        if self.Eini == self.Eupp:      # activates in cases where the initial potential is equal to the upper vertex potential      
            for ix in range(0, self.ns):        # loops through the number of scans
                self.E = np.append(self.E, np.round(np.linspace(self.Eini + (self.window / self.dp), self.Elow, self.dp, endpoint = True), 9))      # adds the negative scan direction portion of the potential window to the potential array (rounded to 9 d.p)
                self.E = np.append(self.E, np.round(np.linspace(self.Elow - (self.window / self.dp), self.Eini, self.dp, endpoint = True), 9))      # adds the positive scan direction portion of the potential window to the potential array (rounded to 9 d.p)

        '''STARTING IN BETWEEN VERTEX POTENTIALS'''
        if self.Elow < self.Eini < self.Eupp:       # activates in cases where the initial potential is between the lower vertex potential and the upper vertex potential  

            '''POSITIVE SCAN DIRECTION'''
            if self.dE > 0:     # activates in cases where the step potential is postive
                for ix in range(0, self.ns):        # loops through the number of scans
                    self.E = np.append(self.E, np.round(np.linspace(self.Eini + (self.window / self.dp), self.Eupp, self.udp, endpoint = True), 9))     # adds the postive scan direction portion of the upper partial potential window to the potential array (rounded to 9 d.p)
                    self.E = np.append(self.E, np.round(np.linspace(self.Eupp - (self.window / self.dp), self.Elow, self.dp, endpoint = True), 9))      # adds the negative scan direction portion of the potential window to the potential array (rounded to 9 d.p)
                    self.E = np.append(self.E, np.round(np.linspace(self.Elow + (self.window / self.dp), self.Eini, self.ldp, endpoint = True), 9))     # adds the positive scan direction portion of the lower partial potential window to the potential array (rounded to 9 d.p)
            
            '''NEGATIVE SCAN DIRECTION'''
            if self.dE < 0:     # activates in cases where the step potential is negative
                for ix in range(0, self.ns):        # loops through the number of scans
                    self.E = np.append(self.E, np.round(np.linspace(self.Eini - (self.window / self.dp), self.Elow, self.ldp, endpoint = True), 9))     # adds the negative scan direction portion of the lower partial potential window to the potential array (rounded to 9 d.p)
                    self.E = np.append(self.E, np.round(np.linspace(self.Elow + (self.window / self.dp), self.Eupp, self.dp, endpoint = True), 9))      # adds the positrive scan direction portion of the potential window to the potential array (rounded to 9 d.p)
                    self.E = np.append(self.E, np.round(np.linspace(self.Eupp + (self.window / self.dp), self.Eini, self.udp, endpoint = True), 9))     # adds the negative scan direction portion of the upper partial potential window to the potential array (rounded to 9 d.p)
        
        self.indexWF = self.index       # exported indexing array
        self.tWF = self.t       # exported time array
        self.EWF = self.E       # exported potential array


      
class CyclicStaircaseVoltammetry(CyclicLinearVoltammetry):

    '''Creates the waveform for a cyclic staircase voltammetry procedure \n
    Requires: \n
    Eini - the initial potential (in V) \n
    Eupp - the upper vertex potential (in V) \n
    Elow - the lower vertex potential (in V) \n
    dE - the step size (in V) \n
    sr - the scan rate (in V/s) \n
    ns - the number of scans \n
    osf - the oscilloscope sampling frequency (in Sa/s)
    '''

    def __init__(self, Eini, Eupp, Elow, dE, sr, ns, osf):
        super().__init__(Eini, Eupp, Elow, dE, sr, ns, osf)     # adopts parameters from the CyclicLinearVoltammetry class

        '''LABELS'''
        self.type = 'staircase'     # label for use in simulations.py
        self.label = 'CSV'      # label for file naming
                      
        '''INDEX'''
        self.indexWF = np.arange(0, round((self.tmax + (self.dE/self.sr)) / self.dt) + (2 * self.ns * self.steps + 1), 1)     # produces a rounded indexing array which accounts for the additional step at the end of the waveform and for staircase points equal to the total number of steps taken (plus one)
        
        '''TIME'''
        self.tWF = np.array([])     # creates an empty time array
        for ix in range(0, 2 * self.ns * self.steps + 1):       # loops through the total number of steps (plus one)
            self.tWF = np.append(self.tWF, np.linspace(0, self.dt * self.interval, self.interval + 1) + ix * self.dt * self.interval)       # creates a temporary time array for a single step, then adds the step time for the current step and appends the result to the time array (the beginning of each temporary array overlaps with the end of the previous one, making a staircase time array)
        
        '''POTENTIAL'''
        self.EWF = np.ones(self.interval + 1) * self.Eini       # creates an array containing as many elements as the interval sampling points (plus one), all equal to the initial potential

        '''STARTING FROM LOWER VERTEX POTENTIAL'''
        if self.Eini == self.Elow:      # activates in cases where the initial potential is equal to the lower vertex potential                   
            for ix in range(0, self.ns):        # loops through the number of scans
                for iy in np.round(np.linspace(self.Eini + self.dE, self.Eupp, self.steps, endpoint = True), 6):        # loops through the positive scan direction portion of the potential window (rounded to 6 d.p)
                    self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # creates an array of each potential with as many elements as the interval sampling points (plus one) and adds it to the potential array
                for iy in np.round(np.linspace(self.Eupp - self.dE, self.Eini, self.steps, endpoint = True), 6):        # loops through the negative scan direction portion of the potential window (rounded to 9 d.p)
                    self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # creates an array of each potential with as many elements as the interval sampling points (plus one) and adds it to the potential array
        
        '''STARTING FROM UPPER VERTEX POTENTIAL'''
        if self.Eini == self.Eupp:      # activates in cases where the initial potential is equal to the upper vertex potential   
            for ix in range(0, self.ns):        # loops through the number of scans
                for iy in np.round(np.linspace(self.Elow - self.dE, self.Eini, self.steps, endpoint = True), 6):        # loops through the negative scan direction portion of the potential window (rounded to 6 d.p)
                    self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # creates an array of each potential with as many elements as the interval sampling points (plus one) and adds it to the potential array
                for iy in np.round(np.linspace(self.Elow - self.dE, self.Eini, self.steps, endpoint = True), 6):       # loops through the positive scan direction portion of the potential window (rounded to 6 d.p)
                    self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # creates an array of each potential with as many elements as the interval sampling points (plus one) and adds it to the potential array
        
        '''STARTING IN BETWEEN VERTEX POTENTIALS'''
        if self.Elow < self.Eini < self.Eupp:       # activates in cases where the initial potential is between the lower vertex potential and the upper vertex potential        
            
            '''POSITIVE SCAN DIRECTION'''
            if self.dE > 0:     # activates in cases where the step potential is positive   
                for ix in range(0, self.ns):        # loops through the number of scans
                    for iy in np.round(np.linspace(self.Eini + self.dE, self.Eupp, self.usteps, endpoint = True), 6):       # loops through the positive scan direction portion of the upper partial potential window (rounded to 6 d.p)
                        self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # creates an array of each potential with as many elements as the interval sampling points (plus one) and adds it to the potential array
                    for iy in np.round(np.linspace(self.Eupp - self.dE, self.Elow, self.steps, endpoint = True), 6):        # loops through the negative scan direction portion of the potential window (rounded to 6 d.p)
                        self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # creates an array of each potential with as many elements as the interval sampling points (plus one) and adds it to the potential array
                    for iy in np.round(np.linspace(self.Elow + self.dE, self.Eini, self.lsteps, endpoint = True), 6):       # loops through the positive scan direction portion of the lower partial potential window (rounded to 6 d.p)
                        self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # creates an array of each potential with as many elements as the interval sampling points (plus one) and adds it to the potential array
            
            '''NEGATIVE SCAN DIRECTION'''
            if self.dE < 0:     # activates in cases where the step potential is negative  
                for ix in range(0, self.ns):        # loops through the number of scans
                    for iy in np.round(np.linspace(self.Eini - self.dE, self.Elow, self.lsteps, endpoint = True), 6):       # loops through the negative scan direction portion of the lower partial potential window (rounded to 6 d.p)
                        self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # adds the negative scan direction portion of the lower partial potential window to the potential array (rounded to 9 d.p)
                    for iy in np.round(np.linspace(self.Elow + self.dE, self.Eupp, self.steps, endpoint = True), 6):        # loops through the positive scan direction portion of the potential window (rounded to 6 d.p)
                        self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # adds the negative scan direction portion of the lower partial potential window to the potential array (rounded to 9 d.p)
                    for iy in np.round(np.linspace(self.Eupp + self.dE, self.Eini, self.usteps, endpoint = True), 6):       # loops through the negative scan direction portion of the upper partial potential window (rounded to 6 d.p)
                        self.EWF = np.append(self.EWF, np.ones(self.interval + 1) * iy)     # adds the negative scan direction portion of the lower partial potential window to the potential array (rounded to 9 d.p)



"""
===================================================================================================
GENERATING WAVEFORMS FROM MAIN
===================================================================================================
"""

if __name__ == '__main__': 
        
    '''1. MAKE A /DATA FOLDER''' 
    cwd = os.getcwd()

    try:
        os.makedirs(cwd + '/data')
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(cwd + '/data'):
            pass
        else: 
            raise

    '''2. DEFINE THE START TIME'''
    start = time.time()  

    '''3. DESCRIBE THE WAVEFORM'''
    #shape = CyclicLinearVoltammetry(Eini = 0.0, Eupp = 0.5, Elow = -0.5, dE = 0.002, sr = 0.5, ns = 1, osf = None)
    shape = CyclicStaircaseVoltammetry(Eini = 0.0, Eupp = 0.5, Elow = -0.5, dE = 0.002, sr = 0.5, ns = 1, osf = None)
    
    '''4. SAVE THE DATA'''
    filepath = f'{cwd}/data/{time.strftime("%Y-%m-%d %H-%M-%S")} {shape.label} waveform.txt'
    with open(filepath, 'w') as file:
        for ix, iy, iz in shape.output():
            file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')

    '''5. DEFINE THE END TIME'''
    end = time.time()
    print(f'The waveform took {end-start} seconds to generate')