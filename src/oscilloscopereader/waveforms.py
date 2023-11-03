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


'''WAVEFORM CLASSES'''
class Waveform:
    '''Parent class for cyclic voltammetry waveforms'''
    def __init__(self, Eini, Eupp, Elow, dE, sr, ns, osf):

        self.Eini = Eini        # Start potential
        self.Eupp = Eupp        # Upper vertex potential
        self.Elow = Elow        # Lower vertex potential
        self.dE = dE            # Potential step size
        self.sr = sr            # Scan rate
        self.ns = ns            # Number of scans
        self.osf = osf          # Oscilloscope sampling frequency
        
        '''DATATYPE ERRORS'''
        if isinstance(self.Eini, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the start potential. Enter either a float or an integer value corresponding to a potential in V.' + '\n')
            sys.exit()
        if isinstance(self.Eupp, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the upper vertex potential. Enter either a float or an integer value corresponding to a potential in V.' + '\n')
            sys.exit()        
        if isinstance(self.Elow, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the lower vertex potential. Enter either a float or an integer value corresponding to a potential in V.' + '\n')
            sys.exit()      
        if isinstance(self.dE, (float)) is False:
            print('\n' + 'An invalid datatype was used for the step potential. Enter a float value corresponding to a potential in V.' + '\n')
            sys.exit()    
        if isinstance(self.sr, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the scan rate. Enter a float or an integer value corresponding to the scan rate in V/s.' + '\n')
            sys.exit() 
        if isinstance(self.ns, (int)) is False:
            print('\n' + 'An invalid datatype was used for the number of scans. Enter an integer value corresponding to the scan rate in V/s.' + '\n')
            sys.exit() 
        if isinstance(self.osf, (int, type(None))) is False:
            print('\n' + 'An invalid datatype was used for the oscilloscope sampling rate. Enter an integer value or None.' + '\n')
            sys.exit()

        '''DATA VALUE ERRORS'''
        if self.Eupp == self.Elow:
            print('\n' + 'Upper and lower vertex potentials must be different values' + '\n')
            sys.exit()
        if self.Eupp < self.Elow:
            print('\n' + 'Upper vertex potential must be greater than lower vertex potential' + '\n')
            sys.exit()  
        if self.Eini < self.Elow:
            print('\n' + 'Start potential must be higher than or equal to the lower vertex potential' + '\n')
            sys.exit()
        if self.Eini > self.Eupp:
            print('\n' + 'Start potential must be lower than or equal to the upper vertex potential' + '\n')
            sys.exit()
        if self.dE == 0:
            print('\n' + 'Step potential must be a non-zero value' + '\n')
            sys.exit()
        if abs(self.dE) > abs(self.Eupp - self.Elow):
            print('\n' + 'Step potential must not be greater than the potential window' + '\n')
            sys.exit()
        if self.Eini == self.Elow and self.dE < 0:
            print('\n' + 'Step potential must be a positive value for a positive scan direction' + '\n')
            sys.exit()
        if self.Eini == self.Eupp and self.dE > 0:
            print('\n' + 'Step potential must be a negative value for a negative scan direction' + '\n')
            sys.exit()
        if self.sr <= 0:
            print('\n' + 'Scan rate must be a positive non-zero value' + '\n')
            sys.exit()
        if self.ns <=0:
            print('\n' + 'Number of scans must be a positive non-zero value' + '\n')
            sys.exit()
        if type(self.osf) == int and self.osf < 1:
            print('\n' + 'Oscilloscope sampling rate must be either between 1 and infinity or set to None' + '\n')
            sys.exit() 
        
        if self.osf == None:
            self.osf = round(np.abs(self.sr / self.dE))

        self.interval = round(np.abs(self.dE / self.sr) * self.osf)

    def output(self):
        '''Function that returns the waveform for checking or data processing purposes'''
        zipped = zip(self.indexWF, self.tWF, self.EWF)
        return zipped


class CyclicLinearVoltammetry(Waveform):
    def __init__(self, Eini, Eupp, Elow, dE, sr, ns, osf):
        super().__init__(Eini, Eupp, Elow, dE, sr, ns, osf)
        
        self.type = 'linear'
        self.label = 'CV'

        '''STARTING FROM LOWER VERTEX POTENTIAL''' 
        if self.Eini == self.Elow:                
            self.window = round(self.Eupp - self.Elow, 3)
            self.dp = round(self.window * self.osf / self.sr)
            self.tmax = round(2 * self.ns * self.window / self.sr, 6)
            self.dt = round((1 / self.osf), 9)
           
            '''INDEX'''
            self.index = np.arange(0, round((self.tmax + self.dt) / self.dt), 1, dtype = np.int32)
        
            '''TIME'''
            self.t = self.index * self.dt 
            
            '''POTENTIAL'''
            self.E = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.E = np.append(self.E, np.round(np.linspace(self.Eini + (self.window / self.dp), self.Eupp, self.dp, endpoint = True, dtype = np.float32), 6))
                self.E = np.append(self.E, np.round(np.linspace(self.Eupp - (self.window / self.dp), self.Eini, self.dp, endpoint = True, dtype = np.float32), 6))

    
        '''STARTING FROM UPPER VERTEX POTENTIAL'''
        if self.Eini == self.Eupp:     
            self.window = round(self.Eupp - self.Elow, 3)
            self.dp = round(self.window * self.osf / self.sr)
            self.tmax = round(2 * self.ns * self.window / self.sr, 6)
            self.dt = round((1 / self.osf), 9)

            '''INDEX'''
            self.index = np.arange(0, round((self.tmax + self.dt) / self.dt), 1, dtype = np.int32)
        
            '''TIME'''
            self.t = self.index * self.dt  
            
            '''POTENTIAL'''
            self.E = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.E = np.append(self.E, np.round(np.linspace(self.Eini + (self.window / self.dp), self.Elow, self.dp, endpoint = True, dtype = np.float32), 6))
                self.E = np.append(self.E, np.round(np.linspace(self.Elow - (self.window / self.dp), self.Eini, self.dp, endpoint = True, dtype = np.float32), 6))


        '''STARTING IN BETWEEN VERTEX POTENTIALS'''
        if self.Elow < self.Eini < self.Eupp:        
            self.uppwindow = round(self.Eupp - self.Eini, 3)
            self.window = round(self.Eupp - self.Elow, 3)
            self.lowwindow = round(self.Eini - self.Elow, 3)
            self.uppdp = round(self.uppwindow * self.osf / self.sr)
            self.dp = round(self.window * self.osf / self.sr)
            self.lowdp = round(self.lowwindow * self.osf / self.sr)
            self.tmax = round(self.ns * (self.uppwindow + self.window + self.lowwindow) / self.sr, 6)
            self.dt = round((1 / self.osf), 9)

            '''INDEX'''
            self.index = np.arange(0, round((self.tmax + self.dt) / self.dt), 1, dtype = np.int32)
        
            '''TIME'''
            self.t = self.index * self.dt
            
            '''POTENTIAL WITH POSITIVE SCAN DIRECTION'''
            if self.dE > 0:
                self.E = np.array([self.Eini])
                for ix in range(0, self.ns):
                    self.E = np.append(self.E, np.round(np.linspace(self.Eini + (self.window / self.dp), self.Eupp, self.uppdp, endpoint = True, dtype = np.float32), 6))
                    self.E = np.append(self.E, np.round(np.linspace(self.Eupp - (self.window / self.dp), self.Elow, self.dp, endpoint = True, dtype = np.float32), 6))
                    self.E = np.append(self.E, np.round(np.linspace(self.Elow + (self.window / self.dp), self.Eini, self.lowdp, endpoint = True, dtype = np.float32), 6))

            '''POTENTIAL WITH NEGATIVE SCAN DIRECTION'''
            if self.dE < 0:
                self.E = np.array([self.Eini])
                for ix in range(0, self.ns):
                    self.E = np.append(self.E, np.round(np.linspace(self.Eini - (self.window / self.dp), self.Elow, self.lowdp, endpoint = True, dtype = np.float32), 6))
                    self.E = np.append(self.E, np.round(np.linspace(self.Elow + (self.window / self.dp), self.Eupp, self.dp, endpoint = True, dtype = np.float32), 6))
                    self.E = np.append(self.E, np.round(np.linspace(self.Eupp + (self.window / self.dp), self.Eini, self.uppdp, endpoint = True, dtype = np.float32), 6))
        

        '''PLOTTING WAVEFORM'''
        self.tPLOT = self.t
        self.EPLOT = self.E


        '''EXPORTED WAVEFORM'''
        self.indexWF = self.index
        self.tWF = self.t
        self.EWF = self.E


      
class CyclicStaircaseVoltammetry(CyclicLinearVoltammetry):
    '''Parent class for all waveforms composed of both steps and sweeps'''
    def __init__(self, Eini, Eupp, Elow, dE, sr, ns, osf):
        super().__init__(Eini, Eupp, Elow, dE, sr, ns, osf)

        self.type = 'staircase'
        self.label = 'CSV'

        '''STARTING FROM LOWER VERTEX POTENTIAL''' 
        if self.Eini == self.Elow:                
            self.dp = round(np.abs(self.window / self.dE))            
            
            '''POTENTIAL'''
            self.E = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.E = np.append(self.E, np.linspace(self.Eini + self.dE, self.Eupp, self.dp, endpoint = True, dtype = np.float32))
                self.E = np.append(self.E, np.linspace(self.Eupp - self.dE, self.Eini, self.dp, endpoint = True, dtype = np.float32))
            self.E = np.round(self.E, 6)

    
        '''STARTING FROM UPPER VERTEX POTENTIAL'''
        if self.Eini == self.Eupp:     
            self.dp = round(np.abs(self.window / self.dE))
                    
            '''POTENTIAL'''
            self.E = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.E = np.append(self.E, np.linspace(self.Eini + self.dE, self.Elow, self.dp, endpoint = True, dtype = np.float32))
                self.E = np.append(self.E, np.linspace(self.Elow - self.dE, self.Eini, self.dp, endpoint = True, dtype = np.float32))
            self.E = np.round(self.E, 6)


        '''STARTING IN BETWEEN VERTEX POTENTIALS'''
        if self.Elow < self.Eini < self.Eupp:        
            self.uppdp = round(np.abs(self.uppwindow / self.dE))
            self.dp = round(np.abs(self.window / self.dE))
            self.lowdp = round(np.abs(self.lowwindow / self.dE))
            
            '''POTENTIAL WITH POSITIVE SCAN DIRECTION'''
            if self.dE > 0:
                self.E = np.array([self.Eini])
                for ix in range(0, self.ns):
                    self.E = np.append(self.E, np.linspace(self.Eini + self.dE, self.Eupp, self.uppdp, endpoint = True, dtype = np.float32))
                    self.E = np.append(self.E, np.linspace(self.Eupp - self.dE, self.Elow, self.dp, endpoint = True, dtype = np.float32))
                    self.E = np.append(self.E, np.linspace(self.Elow + self.dE, self.Eini, self.lowdp, endpoint = True, dtype = np.float32))


            '''POTENTIAL WITH NEGATIVE SCAN DIRECTION'''
            if self.dE < 0:
                self.E = np.array([self.Eini])
                for ix in range(0, self.ns):
                    self.E = np.append(self.E, np.linspace(self.Eini - self.dE, self.Elow, self.lowdp, endpoint = True, dtype = np.float32))
                    self.E = np.append(self.E, np.linspace(self.Elow + self.dE, self.Eupp, self.dp, endpoint = True, dtype = np.float32))
                    self.E = np.append(self.E, np.linspace(self.Eupp + self.dE, self.Eini, self.uppdp, endpoint = True, dtype = np.float32))
            
        
        '''EXPORTED WAVEFORM'''
        self.indexWF = np.arange(0, round((2 * self.dp + 1) * self.interval), 1, dtype = np.int32)
        self.tWF = np.array([])
        for ix in range(0, 2 * self.dp + 1):
            if ix == 0:
                self.tWF = np.append(self.tWF, self.index[ix * self.interval: (ix + 1) * self.interval] * self.dt)
            else:
                self.tWF = np.append(self.tWF, self.index[ix * self.interval: (ix + 1) * self.interval] * self.dt)
        self.EWF = np.array([])
        for ix in self.E:
            self.EWF = np.append(self.EWF, np.ones(self.interval) * ix)

        pass

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
    #wf = CyclicLinearVoltammetry(Eini = 0, Eupp = 0.5, Elow = 0, dE = 0.002, sr = 0.5, ns = 1, osf = None)
    wf = CyclicStaircaseVoltammetry(Eini = 0, Eupp = 0.5, Elow = 0, dE = 0.002, sr = 0.5, ns = 1, osf = None)
    
    '''4. DEFINE THE END TIME'''
    end = time.time()
    print(f'The waveform took {end-start} seconds to generate')

    '''5. SAVE THE DATA'''
    filepath = f'{cwd}/data/{time.strftime("%Y-%m-%d %H-%M-%S")} {wf.label} waveform.txt'
    with open(filepath, 'w') as file:
        for ix, iy, iz in wf.output():
            file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')