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

Filename:           simulations.py

===================================================================================================

Description:

This file contains the code used by the oscilloscope-reader package to generate simulated data for
capactive charging using an instance of either the CyclicLinearVoltammetry class or the 
CyclicStaircaseVoltammetry class from the waveforms.py file.

===================================================================================================

How to use this file:
    
Whilst this file is designed for use by the operations.py file, it can also be used on its own in 
order to visualise and analyse the effect of staircase waveforms on the analogue current.

In order to use this file:
    1. Scroll down the the bottom of the file, to the 'RUNNING SIMULATIONS FROM MAIN' section.
    2. In the third point of this section, choose the waveform you want to use, commenting out the 
       other waveform
    3. Edit the parameters of this waveform, keeping the following rules in mind
        a) If you want a scan going in the negative direction, use a negative dE value. 
        b) Negative dE values cannot be used when the start potential is the lower vertex potential
        c) Positive dE values cannot be used when the start potential is the upper vertex potential
        d) An oscilloscope sampling frequency (osf) of None gives a data point for each dE value
        e) Increasing the osf will increase the number of data points for each dE
        f) The osf cannot be set below the natural sampling frequency (given by sr/dE)
    4. In the fourth point of this section, choose the time constant parameters you want for the 
       generated data
    5. Run the python file

The simulated data will be saved in a .txt file in the /data folder of the current working
directory.

===================================================================================================
'''


import sys
import os
import time
import numpy as np
from errno import EEXIST
import waveforms as wf


class Capacitance:
    
    '''Creates a basic simulation of capacitive charging based on the nature of an imported potential waveform \n
    
    Requires: \n
    shape - an instance of one of the potential waveform classes from the waveforms.py file \n
    Cd - double layer capacitance (in F) \n
    Ru - uncompensated resistance (in Ω) \n'''

    def __init__(self, shape, Cd = 0.000050, Ru = 500):
        
        self.label = 'simulated'

        self.shape = shape
        self.Eini = shape.Eini        # Start potential in V
        self.Eupp = shape.Eupp        # Upper vertex potential in V
        self.Elow = shape.Elow        # Lower vertex potential in V
        self.dE = shape.dE            # Step size in V
        self.sr = shape.sr            # Scan rate in V/s
        self.ns = shape.ns            # Number of scans (no unit)
        self.osf = shape.osf          # Oscilloscope sampling frequency

        self.Cd = Cd            # Double layer capacitance in F
        self.Ru = Ru            # Uncompensated resistance in Ohms
        
        if self.shape.type == 'linear':
            self.simple()
        if self.shape.type == 'staircase':
            self.detailed() 

    def simple(self):
        '''Returns E vs. i for a CV performed on a capacitor with parameters derived from the Capacitance() class\n
        Uses equation 1.6.23 from the 3rd edition of Electrochemical Methods:\n
        i = sr*Cd*(1-np.exp(-t/(Ru*Cd)))'''
        
        self.i = np.array([])
        
        if self.Eini == self.Elow:
            for iy in range(0, self.ns):
                self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
                self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
        
        if self.Eini == self.Eupp:
            for iy in range(0, self.ns):
                self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
                self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
        
        if self.Elow < self.Eini < self.Eupp:  
            if self.dE > 0:
                for iy in range(0, self.ns):
                    if iy == 0:
                        self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.udp]) / (self.Ru * self.Cd))))
                        self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
                    else:
                        self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
                        self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
                
                self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.ldp]) / (self.Ru * self.Cd))))

            if self.dE < 0:
                for iy in range(0, self.ns):
                    if iy == 0:
                        self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.ldp]) / (self.Ru * self.Cd))))
                        self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
                    else:
                        self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
                        self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.dp]) / (self.Ru * self.Cd))))
                
                self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.shape.t[:self.shape.udp]) / (self.Ru * self.Cd))))
        
        self.E = self.shape.E[:self.i.size]


    def detailed(self):
        '''Returns E vs. i for a CSV performed on a capacitor with parameters derived from the Capacitance() class\n
        Uses equation 1.6.17 from the 3rd edition of Electrochemical Methods:\n
        i = (dE/Ru)*np.exp(-t/(Ru*Cd))'''   
        
        self.i = np.array([])
        self.iplus = np.zeros(self.shape.dp)#dp is different here
        self.iminus = np.zeros(self.shape.dp)        
        
        if self.Eini == self.Elow:
            for ix in range(0, self.ns):
                for iy in range(0, self.shape.steps):#from here
                    space = int(iy * self.shape.interval)
                    self.iplus[space:] = np.add(self.iplus[space:], (self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                for iy in range(0, self.shape.steps):
                    space = int(iy * self.shape.interval)
                    self.iminus[space:] = np.add(self.iminus[space:], (-self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                self.i = np.append(self.i, self.iplus)
                self.i = np.append(self.i, self.iminus)
                self.iplus = np.zeros(self.shape.dp)
                self.iminus = np.zeros(self.shape.dp)

        if self.Eini == self.Eupp:
            for ix in range(0, self.ns):
                for iy in range(0, self.shape.steps):
                    space = int(iy * self.shape.interval)
                    self.iminus[space:] = np.add(self.iminus[space:], (self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                for iy in range(0, self.shape.steps):
                    space = int(iy * self.shape.interval)
                    self.iplus[space:] = np.add(self.iplus[space:], (-self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                self.i = np.append(self.i, self.iminus)
                self.i = np.append(self.i, self.iplus)
                self.iplus = np.zeros(self.shape.dp)
                self.iminus = np.zeros(self.shape.dp)

        if self.Elow < self.Eini < self.Eupp:  
            self.iupp = np.zeros(self.shape.udp)
            self.ilow = np.zeros(self.shape.ldp)        

            if self.dE > 0:
                for ix in range(0, self.ns):
                    if ix == 0:
                        for iy in range(0, self.shape.usteps):
                            space = int(iy * self.shape.interval)
                            self.iupp[space:] = np.add(self.iupp[space:], (self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.udp - space]) / (self.Ru * self.Cd)))
                        for iy in range(0, self.shape.steps):
                            space = int(iy * self.shape.interval)
                            self.iminus[space:] = np.add(self.iminus[space:], (-self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                        
                        self.i = np.append(self.i, self.iupp)
                        self.i = np.append(self.i, self.iminus)
                        self.iminus = np.zeros(self.shape.dp)

                    else:
                        for iy in range(0, self.shape.steps):
                            space = int(iy * self.shape.interval)
                            self.iplus[space:] = np.add(self.iplus[space:], (self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                        for iy in range(0, self.shape.steps):
                            space = int(iy * self.shape.interval)
                            self.iminus[space:] = np.add(self.iminus[space:], (-self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                        
                        self.i = np.append(self.i, self.iplus)
                        self.i = np.append(self.i, self.iminus)
                        self.iplus = np.zeros(self.shape.dp)
                        self.iminus = np.zeros( self.shape.dp)

                for iz in range(0, self.shape.lsteps):
                    space = int(iz * self.shape.interval)
                    self.ilow[space:] = np.add(self.ilow[space:], (self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.ldp - space]) / (self.Ru * self.Cd)))
                        
                self.i = np.append(self.i, self.ilow)

            if self.dE < 0:
                for ix in range(0, self.ns):
                    if ix == 0:
                        for iy in range(0, self.shape.lsteps):
                            space = int(iy * self.shape.interval)
                            self.ilow[space:] = np.add(self.ilow[space:], (self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.ldp - space]) / (self.Ru * self.Cd)))
                        for iy in range(0, self.shape.steps):
                            space = int(iy * self.shape.interval)
                            self.iplus[space:] = np.add(self.iplus[space:], (-self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                        
                        self.i = np.append(self.i, self.ilow)
                        self.i = np.append(self.i, self.iplus)
                        self.iplus = np.zeros(self.shape.dp)

                    else:
                        for iy in range(0, self.shape.steps):
                            space = int(iy * self.shape.interval)
                            self.iminus[space:] = np.add(self.iminus[space:], (self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                        for iy in range(0, self.shape.steps):
                            space = int(iy * self.shape.interval)
                            self.iplus[space:] = np.add(self.iplus[space:], (-self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.dp - space]) / (self.Ru * self.Cd)))
                        
                        self.i = np.append(self.i, self.iminus)
                        self.i = np.append(self.i, self.iplus)
                        self.iminus = np.zeros(self.shape.dp)
                        self.iplus = np.zeros(self.shape.dp)

                for iz in range(0, self.shape.usteps):
                    space = int(iz * self.shape.interval)
                    self.iupp[space:] = np.add(self.iupp[space:], (self.dE/self.Ru) * np.exp((-self.shape.t[:self.shape.udp - space]) / (self.Ru * self.Cd)))
                        
                self.i = np.append(self.i, self.iupp)

    
    def output(self):
        '''Returns the simulated data for checking or analysis purposes'''
        zipped = zip(self.shape.t, self.shape.E, self.i)
        return zipped


"""
===================================================================================================
RUNNING SIMULATIONS FROM MAIN
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
    #shape = wf.CyclicLinearVoltammetry(Eini = 0, Eupp = 0.5, Elow = -0.50, dE = -0.002, sr = 0.5, ns = 1, osf = 4000)
    shape = wf.CyclicStaircaseVoltammetry(Eini = -0.3, Eupp = 0.8, Elow = -0.65, dE = 0.002, sr = 0.5, ns = 1, osf = 2000000)
    
    '''4. DESCRIBE THE SIMULATION CONDITIONS'''
    data = Capacitance(shape, Cd = 0.00010, Ru = 750)

    '''5. SAVE THE DATA'''
    filepath = f'{cwd}/data/{time.strftime("%Y-%m-%d %H-%M-%S")} {shape.type} waveform.txt'
    with open(filepath, 'w') as file:
        for ix, iy, iz in data.output():
            file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')
    
    '''6. DEFINE THE END TIME'''
    end = time.time()
    print(f'The simulation took {end-start} seconds to complete')

