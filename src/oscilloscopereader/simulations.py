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

from errno import EEXIST

import waveforms as wf


class Capacitance:
    '''Write something here'''
    def __init__(self, input, Cd = 0.000050, Ru = 500):
        
        self.type = 'simulated'

        self.input = input
        self.Eini = input.Eini        # Start potential in V
        self.Eupp = input.Eupp        # Upper vertex potential in V
        self.Elow = input.Elow        # Lower vertex potential in V
        self.dE = input.dE            # Step size in V
        self.sr = input.sr            # Scan rate in V/s
        self.ns = input.ns            # Number of scans (no unit)
        self.osf = input.osf          # Oscilloscope sampling frequency

        self.Cd = Cd            # Double layer capacitance in F
        self.Ru = Ru            # Uncompensated resistance in Ohms

        self.cf = -1       
        
        if self.input.type == 'linear':
            self.simple()
        if self.input.type == 'staircase':
            self.detailed() 

    def simple(self):
        '''Returns E vs. i for a CV performed on a capacitor with parameters derived from the Capacitance() class\n
        Uses equation 1.6.23 from the 3rd edition of Electrochemical Methods:\n
        i = sr*Cd*(1-np.exp(-t/(Ru*Cd)))'''
        
        self.i = np.array([])
        
        if self.Eini == self.Elow:
            for iy in range(0, self.ns):
                self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
                self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
        
        if self.Eini == self.Eupp:
            for iy in range(0, self.ns):
                self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
                self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
        
        if self.Elow < self.Eini < self.Eupp:  
            if self.dE > 0:
                for iy in range(0, self.ns):
                    if iy == 0:
                        self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.udp]) / (self.Ru * self.Cd))))
                        self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
                    else:
                        self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
                        self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
                
                self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.ldp]) / (self.Ru * self.Cd))))

            if self.dE < 0:
                for iy in range(0, self.ns):
                    if iy == 0:
                        self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.ldp]) / (self.Ru * self.Cd))))
                        self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
                    else:
                        self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
                        self.i = np.append(self.i, self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.dp]) / (self.Ru * self.Cd))))
                
                self.i = np.append(self.i, -self.sr * self.Cd * (1 - np.exp((-self.input.t[:self.input.udp]) / (self.Ru * self.Cd))))
        
        self.E = self.input.E[:self.i.size]


    def detailed(self):
        '''Returns E vs. i for a CSV performed on a capacitor with parameters derived from the Capacitance() class\n
        Uses equation 1.6.17 from the 3rd edition of Electrochemical Methods:\n
        i = (dE/Ru)*np.exp(-t/(Ru*Cd))'''   
        
        self.i = np.array([])
        self.iplus = np.zeros(self.input.dp)#dp is different here
        self.iminus = np.zeros(self.input.dp)        
        
        if self.Eini == self.Elow:
            for ix in range(0, self.ns):
                for iy in range(0, self.input.steps):#from here
                    space = int(iy * self.input.interval)
                    self.iplus[space:] = np.add(self.iplus[space:], (self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                for iy in range(0, self.input.steps):
                    space = int(iy * self.input.interval)
                    self.iminus[space:] = np.add(self.iminus[space:], (-self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                self.i = np.append(self.i, self.iplus)
                self.i = np.append(self.i, self.iminus)
                self.iplus = np.zeros(self.input.dp)
                self.iminus = np.zeros(self.input.dp)

        if self.Eini == self.Eupp:
            for ix in range(0, self.ns):
                for iy in range(0, self.input.steps):
                    space = int(iy * self.input.interval)
                    self.iminus[space:] = np.add(self.iminus[space:], (-self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                for iy in range(0, self.input.steps):
                    space = int(iy * self.input.interval)
                    self.iplus[space:] = np.add(self.iplus[space:], (self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                self.i = np.append(self.i, self.iminus)
                self.i = np.append(self.i, self.iplus)
                self.iplus = np.zeros(self.input.dp)
                self.iminus = np.zeros(self.input.dp)

        if self.Elow < self.Eini < self.Eupp:  
            self.iupp = np.zeros(self.input.udp)
            self.ilow = np.zeros(self.input.ldp)        

            if self.dE > 0:
                for ix in range(0, self.ns):
                    if ix == 0:
                        for iy in range(0, self.input.usteps):
                            space = int(iy * self.input.interval)
                            self.iupp[space:] = np.add(self.iupp[space:], (self.dE/self.Ru) * np.exp((-self.input.t[:self.input.udp - space]) / (self.Ru * self.Cd)))
                        for iy in range(0, self.input.steps):
                            space = int(iy * self.input.interval)
                            self.iminus[space:] = np.add(self.iminus[space:], (-self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                        
                        self.i = np.append(self.i, self.iupp)
                        self.i = np.append(self.i, self.iminus)
                        self.iminus = np.zeros(self.input.dp)

                    else:
                        for iy in range(0, self.input.steps):
                            space = int(iy * self.input.interval)
                            self.iplus[space:] = np.add(self.iplus[space:], (self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                        for iy in range(0, self.input.steps):
                            space = int(iy * self.input.interval)
                            self.iminus[space:] = np.add(self.iminus[space:], (-self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                        
                        self.i = np.append(self.i, self.iplus)
                        self.i = np.append(self.i, self.iminus)
                        self.iplus = np.zeros(self.input.dp)
                        self.iminus = np.zeros( self.input.dp)

                for iz in range(0, self.input.lsteps):
                    space = int(iz * self.input.interval)
                    self.ilow[space:] = np.add(self.ilow[space:], (self.dE/self.Ru) * np.exp((-self.input.t[:self.input.ldp - space]) / (self.Ru * self.Cd)))
                        
                self.i = np.append(self.i, self.ilow)

            if self.dE < 0:
                for ix in range(0, self.ns):
                    if ix == 0:
                        for iy in range(0, self.input.lsteps):
                            space = int(iy * self.input.interval)
                            self.ilow[space:] = np.add(self.ilow[space:], (-self.dE/self.Ru) * np.exp((-self.input.t[:self.input.ldp - space]) / (self.Ru * self.Cd)))
                        for iy in range(0, self.input.steps):
                            space = int(iy * self.input.interval)
                            self.iplus[space:] = np.add(self.iplus[space:], (self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                        
                        self.i = np.append(self.i, self.ilow)
                        self.i = np.append(self.i, self.iplus)
                        self.iplus = np.zeros(self.input.dp)

                    else:
                        for iy in range(0, self.input.steps):
                            space = int(iy * self.input.interval)
                            self.iminus[space:] = np.add(self.iminus[space:], (-self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                        for iy in range(0, self.input.steps):
                            space = int(iy * self.input.interval)
                            self.iplus[space:] = np.add(self.iplus[space:], (self.dE/self.Ru) * np.exp((-self.input.t[:self.input.dp - space]) / (self.Ru * self.Cd)))
                        
                        self.i = np.append(self.i, self.iminus)
                        self.i = np.append(self.i, self.iplus)
                        self.iminus = np.zeros(self.input.dp)
                        self.iplus = np.zeros(self.input.dp)

                for iz in range(0, self.input.usteps):
                    space = int(iz * self.input.interval)
                    self.iupp[space:] = np.add(self.iupp[space:], (-self.dE/self.Ru) * np.exp((-self.input.t[:self.input.udp - space]) / (self.Ru * self.Cd)))
                        
                self.i = np.append(self.i, self.iupp)

    
    def output(self):
        '''Returns the simulated data for checking or analysis purposes'''
        zipped = zip(self.input.t, self.input.E, self.i)
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
    #shape = wf.CyclicLinearVoltammetry(Eini = 0, Eupp = 0.5, Elow = 0, dE = 0.002, sr = 0.5, ns = 1, osf = None)
    shape = wf.CyclicStaircaseVoltammetry(Eini = 0, Eupp = 0.5, Elow = -0.5, dE = -0.002, sr = 0.5, ns = 1, osf = 4000)
    
    '''4. DESCRIBE THE SIMULATION CONDITIONS'''
    input = Capacitance(shape, Cd = 0.00010, Ru = 750)

    '''5. SAVE THE DATA'''
    filepath = f'{cwd}/data/{time.strftime("%Y-%m-%d %H-%M-%S")} {shape.type} waveform.txt'
    with open(filepath, 'w') as file:
        for ix, iy, iz in input.output():
            file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')
    
    '''6. DEFINE THE END TIME'''
    end = time.time()
    print(f'The simulation took {end-start} seconds to complete')

