import sys
import os
import time
import numpy as np

from errno import EEXIST


'''PARENT CLASSES'''
class sweep:
    '''Parent class for all sweep type waveforms'''
    def __init__(self, Eini, Eupp, Elow, dE, sr, ns):
        
        self.type = 'sweep'

        self.Eini = Eini        # Start potential
        self.Eupp = Eupp        # Upper vertex potential
        self.Elow = Elow        # Lower vertex potential
        self.dE = dE            # Step size (i.e. the number of data points)
        self.sr = sr            # Scan rate
        self.ns = ns            # Number of scans for cyclic voltammetry

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

    def output(self):
        '''Function that returns the waveform for checking or data processing purposes'''
        zipped = zip(self.indexWF, self.tWF, self.EWF)
        return zipped
                
class hybrid:
    '''Parent class for all waveforms composed of both steps and sweeps'''
    def __init__(self, Eini, Eupp, Elow, dE, sr, ns, st, detailed):

        self.type = 'hybrid'

        self.Eini = Eini        # Start potential for sweeping step techniques
        self.Eupp = Eupp        # Upper vertex potential for sweeping step techniques
        self.Elow = Elow        # Lower vertex potential for sweeping step techniques
        self.dE = dE            # Step size for sweeping step techniques
        self.sr = sr            # Scan rate for sweeping step techniques
        self.ns = ns            # Number of scans for cyclic staircase voltammetry
        self.st = st            # Sampling time

        self.detailed = detailed

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
        if isinstance(self.st, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the sampling time. Enter either a float or an integer value corresponding to a time in s.' + '\n')
            sys.exit()
        if isinstance(self.detailed, (bool)) is False:
            print('\n' + 'An invalid datatype was used for the detailed argument. Enter either True or False.' + '\n')
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
        if self.st <= 0:
            print('\n' + 'Sampling time must be a positive non-zero value' + '\n')
            sys.exit()
    
    def output(self):
        '''Function that returns the waveform for checking or data processing purposes'''
        zipped = zip(self.indexWF, self.tWF, self.EWF)
        return zipped


'''WAVEFORM CLASSES'''
class CV(sweep):
    '''Waveform for cyclic voltammetry \n
    \n
    Eini - start potential \n
    Eupp - upper vertex potential \n
    Elow - lower vertex potential \n
    dE   - step size (in this case, number of data points) \n
    sr   - scan rate \n
    ns   - number of scans'''

    def __init__(self, Eini, Eupp, Elow, dE, sr, ns):
        super().__init__(Eini, Eupp, Elow, dE, sr, ns)

        self.subtype = 'CV'

        '''STARTING FROM LOWER VERTEX POTENTIAL''' 
        if self.Eini == self.Elow:                
            self.window = round(self.Eupp - self.Elow, 3)
            self.dp = round(np.abs(self.window / self.dE))
            self.tmax = round(2 * self.ns * self.window / self.sr, 6)
            self.dt = round(np.abs(self.dE / self.sr), 9)

            '''INDEX'''
            self.index = np.arange(0, round((self.tmax + self.dt) / self.dt, 9), 1, dtype = np.int32)
        
            '''TIME'''
            self.t = self.index * self.dt
            
            '''POTENTIAL'''
            self.E = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.E = np.append(self.E, np.round(np.linspace(self.Eini + self.dE, self.Eupp, self.dp, endpoint = True, dtype = np.float32), 3))
                self.E = np.append(self.E, np.round(np.linspace(self.Eupp - self.dE, self.Eini, self.dp, endpoint = True, dtype = np.float32), 3))

    
        '''STARTING FROM UPPER VERTEX POTENTIAL'''
        if self.Eini == self.Eupp:     
            self.window = round(self.Eupp - self.Elow, 3)
            self.dp = round(np.abs(self.window / self.dE))
            self.tmax = round(2 * self.ns * self.window / self.sr, 6)
            self.dt = round(np.abs(self.dE / self.sr), 9)

            '''INDEX'''
            self.index = np.arange(0, round((self.tmax + self.dt) / self.dt, 9), 1, dtype = np.int32)
        
            '''TIME'''
            self.t = self.index * self.dt
            
            '''POTENTIAL'''
            self.E = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.E = np.append(self.E, np.round(np.linspace(self.Eini + self.dE, self.Elow, self.dp, endpoint = True, dtype = np.float32), 3))
                self.E = np.append(self.E, np.round(np.linspace(self.Elow - self.dE, self.Eini, self.dp, endpoint = True, dtype = np.float32), 3))


        '''STARTING IN BETWEEN VERTEX POTENTIALS'''
        if self.Elow < self.Eini < self.Eupp:        
            self.uppwindow = round(self.Eupp - self.Eini, 3)
            self.window = round(self.Eupp - self.Elow, 3)
            self.lowwindow = round(self.Eini - self.Elow, 3)
            self.uppdp = round(np.abs(self.uppwindow / self.dE))
            self.dp = round(np.abs(self.window / self.dE))
            self.lowdp = round(np.abs(self.lowwindow / self.dE))
            self.tmax = round(self.ns * (self.uppwindow + self.window + self.lowwindow) / self.sr, 6)
            self.dt = round(np.abs(self.dE / self.sr), 9)

            '''INDEX'''
            self.index = np.arange(0, round((self.tmax + self.dt) / self.dt, 9), 1, dtype = np.int32)
        
            '''TIME'''
            self.t = self.index * self.dt
            
            '''POTENTIAL WITH POSITIVE SCAN DIRECTION'''
            if self.dE > 0:
                self.E = np.array([self.Eini])
                for ix in range(0, self.ns):
                    self.E = np.append(self.E, np.round(np.linspace(self.Eini + self.dE, self.Eupp, self.uppdp, endpoint = True, dtype = np.float32), 3))
                    self.E = np.append(self.E, np.round(np.linspace(self.Eupp - self.dE, self.Elow, self.dp, endpoint = True, dtype = np.float32), 3))
                    self.E = np.append(self.E, np.round(np.linspace(self.Elow + self.dE, self.Eini, self.lowdp, endpoint = True, dtype = np.float32), 3))

            '''POTENTIAL WITH NEGATIVE SCAN DIRECTION'''
            if self.dE < 0:
                self.E = np.array([self.Eini])
                for ix in range(0, self.ns):
                    self.E = np.append(self.E, np.round(np.linspace(self.Eini - self.dE, self.Elow, self.lowdp, endpoint = True, dtype = np.float32), 3))
                    self.E = np.append(self.E, np.round(np.linspace(self.Elow + self.dE, self.Elow, self.dp, endpoint = True, dtype = np.float32), 3))
                    self.E = np.append(self.E, np.round(np.linspace(self.Elow + self.dE, self.Eini, self.uppdp, endpoint = True, dtype = np.float32), 3))
            
        '''PLOTTING WAVEFORM'''
        self.tPLOT = self.t
        self.EPLOT = self.E

        '''EXPORTED WAVEFORM'''
        self.indexWF = self.index
        self.tWF = self.t        
        self.EWF = self.E


class CSV(hybrid):
    '''Waveform for cyclic staircase voltammetry \n   
    \n
    Eini - start potential \n
    Eupp - upper vertex potential \n
    Elow - lower vertex potential \n
    dE   - step size \n
    sr   - scan rate \n
    ns   - number of scans \n
    st   - sampling time'''
    def __init__(self, Eini, Eupp, Elow, dE, sr, ns, st, detailed):
        super().__init__(Eini, Eupp, Elow, dE, sr, ns, st, detailed)
        
        self.subtype = 'CSV'

        '''STARTING FROM LOWER VERTEX POTENTIAL''' 
        if self.Eini == self.Elow:                
            self.window = round(self.Eupp - self.Elow, 3)
            self.dp = round(np.abs(self.window / self.dE))
            self.tmax = round(2 * self.ns * self.window / self.sr, 6)
            self.dt = round(np.abs(self.dE / self.sr), 9)
            self.sp = round(self.dt / self.st)

            '''INDEX'''
            self.index = np.arange(0, round((self.tmax + self.dt) / self.dt, 9), 1, dtype = np.int32)
        
            '''TIME'''
            self.t = self.index * self.dt
            
            '''POTENTIAL'''
            self.E = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.E = np.append(self.E, np.linspace(self.Eini + self.dE, self.Eupp, self.dp, endpoint = True, dtype = np.float32))
                self.E = np.append(self.E, np.linspace(self.Eupp - self.dE, self.Eini, self.dp, endpoint = True, dtype = np.float32))
            self.E = np.round(self.E, 6)

    
        '''STARTING FROM UPPER VERTEX POTENTIAL'''
        if self.Eini == self.Eupp:     
            self.window = round(self.Eupp - self.Elow, 3)
            self.dp = round(np.abs(self.window / self.dE))
            self.tmax = round(2 * self.ns * self.window / self.sr, 6)
            self.dt = round(np.abs(self.dE / self.sr), 9)
            self.sp = round(self.dt / self.st)

            '''INDEX'''
            self.index = np.arange(0, round((self.tmax + self.dt) / self.dt, 9), 1, dtype = np.int32)
        
            '''TIME'''
            self.t = self.index * self.dt
            
            '''POTENTIAL'''
            self.E = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.E = np.append(self.E, np.linspace(self.Eini + self.dE, self.Elow, self.dp, endpoint = True, dtype = np.float32))
                self.E = np.append(self.E, np.linspace(self.Elow - self.dE, self.Eini, self.dp, endpoint = True, dtype = np.float32))
            self.E = np.round(self.E, 6)


        '''STARTING IN BETWEEN VERTEX POTENTIALS'''
        if self.Elow < self.Eini < self.Eupp:        
            self.uppwindow = round(self.Eupp - self.Eini, 3)
            self.window = round(self.Eupp - self.Elow, 3)
            self.lowwindow = round(self.Eini - self.Elow, 3)
            self.uppdp = round(np.abs(self.uppwindow / self.dE))
            self.dp = round(np.abs(self.window / self.dE))
            self.lowdp = round(np.abs(self.lowwindow / self.dE))
            self.tmax = round(self.ns * (self.uppwindow + self.window + self.lowwindow) / self.sr, 6)
            self.dt = round(np.abs(self.dE / self.sr), 9)
            self.sp = round(self.dt / self.st)

            '''INDEX'''
            self.index = np.arange(0, round((self.tmax + self.dt) / self.dt, 9), 1, dtype = np.int32)
        
            '''TIME'''
            self.t = self.index * self.dt
            
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
                    self.E = np.append(self.E, np.linspace(self.Elow + self.dE, self.Elow, self.dp, endpoint = True, dtype = np.float32))
                    self.E = np.append(self.E, np.linspace(self.Elow + self.dE, self.Eini, self.uppdp, endpoint = True, dtype = np.float32))
            
            self.E = np.round(self.E, 6)
        

        '''PLOTTING WAVEFORM'''
        if self.detailed == False:
            self.tPLOT = self.t
            self.EPLOT = self.E

        if self.detailed == True:
            self.tPLOT = np.array([])
            for ix in range(0, self.t.size):
                try:
                    self.tPLOT = np.append(self.tPLOT, np.linspace(self.t[ix], self.t[ix + 1], self.sp, endpoint = False))
                except:
                    self.tPLOT = np.append(self.tPLOT, np.linspace(self.t[ix], self.t[ix] + self.dt, self.sp, endpoint = False))
            self.tPLOT = np.round(self.tPLOT, 9)

            self.EPLOT = np.array([])
            for iy in range(0, self.E.size):
                try:
                    self.EPLOT = np.append(self.EPLOT, np.linspace(self.E[iy], self.E[iy + 1], self.sp, endpoint = False))
                except:
                    self.EPLOT = np.append(self.EPLOT, np.linspace(self.E[iy], self.E[iy] + self.dE, self.sp, endpoint = False))
            self.EPLOT = np.round(self.EPLOT, 9)

    
        '''EXPORTED WAVEFORM'''
        self.indexWF = np.arange(0, self.sp * round((self.tmax + self.dt) / self.dt, 9), 1, dtype = np.int32)
        self.tWF = (self.indexWF * self.dt) / self.sp        
        self.EWF = np.array([])
        for ix in range(0, self.E.size):
            self.EWF = np.append(self.EWF, np.ones((self.sp)) * self.E[ix])
        pass



if __name__ == '__main__': 
        
    start = time.time()    
    cwd = os.getcwd()

    try:
        os.makedirs(cwd + '/data')
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(cwd + '/data'):
            pass
        else: 
            raise
    filepath = cwd + '/data/' + 'waveform.txt'

    #wf = CV(Eini = 0.2, Eupp = 0.8, Elow = 0.2, dE = 0.002, sr = 0.05, ns  = 2)
    wf = CSV(Eini = 0, Eupp = 0.5, Elow = 0, dE = 0.01, sr = 0.1, ns = 1, st = 0.001, detailed = False)

    with open(filepath, 'w') as file:
        for ix, iy, iz in wf.output():
            file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')

    end = time.time()
    print(f'The simulation took {end-start} seconds to complete')