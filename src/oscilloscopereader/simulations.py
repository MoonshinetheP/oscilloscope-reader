import sys
import numpy as np

class Capacitance:
    '''Simulates the charging of a double layer when using CV or CSV \n 
    Also takes input parameters and uses them to create potential waveforms for CV and CSV'''
    
    def __init__(self, Eini = 0.0, Eupp = 0.5, Elow = -0.5, dE = 0.001 , sr = 0.1, ns = 1, Cd = 0.000050, Ru = 500, sp = 1000):
        '''Defines the parameters of the simulation, checks for errors, and makes a potential waveform to be used by other functions'''
        
        self.Eini = Eini        # Start potential in V
        self.Eupp = Eupp        # Upper vertex potential in V
        self.Elow = Elow        # Lower vertex potential in V
        self.dE = dE        # Step size in V
        self.sr = sr        # Scan rate in V/s
        self.ns = ns        # Number of scans (no unit)
        self.Cd = Cd        # Double layer capacitance in F
        self.Ru = Ru        # Uncompensated resistance in Ohms
        self.sp = sp        # Number of data points in a step (no unit)


        '''Datatype errors'''
        if isinstance(self.Eini, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the start potential. Enter either a float or an integer.' + '\n')
            sys.exit()
        if isinstance(self.Eupp, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the upper vertex potential. Enter either a float or an integer.' + '\n')
            sys.exit()        
        if isinstance(self.Elow, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the lower vertex potential. Enter either a float or an integer.' + '\n')
            sys.exit()        
        if isinstance(self.dE, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the step potential. Enter either a float or an integer.' + '\n')
            sys.exit()
        if isinstance(self.sr, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the scan rate. Enter either a float or an integer.' + '\n')
            sys.exit()
        if isinstance(self.ns, (int)) is False:
            print('\n' + 'An invalid datatype was used for the number of scans. Enter an integer.' + '\n')
            sys.exit()
        if isinstance(self.Cd, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the double layer capacitance. Enter either a float or an integer.' + '\n')
            sys.exit()
        if isinstance(self.Ru, (float, int)) is False:
            print('\n' + 'An invalid datatype was used for the uncompensated resistance. Enter either a float or an integer.' + '\n')
            sys.exit()
        if isinstance(self.sp, (int)) is False:
            print('\n' + 'An invalid datatype was used for the number of data points in a step. Enter an integer.' + '\n')
            sys.exit()


        '''Data value errors'''
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
        if self.Cd <= 0:
            print('\n' + 'Double layer capacitance must be a positive non-zero value' + '\n')
            sys.exit()
        if self.Ru <= 0:
            print('\n' + 'Uncompensated resistance must be a positive non-zero value' + '\n')
            sys.exit()
        if self.sp <= 0:
            print('\n' + 'Number of data points in a step must be a positive non-zero value' + '\n')
            sys.exit()


        '''Waveform generation'''        
        if self.Eini == self.Elow:          
            self.segments = 2 * self.ns          # Number of segments expected          
            self.window = self.Eupp - self.Elow         # Potential window of each segment
            self.dp = int(self.window/self.dE)       # Number of data points in each potential window
            
            self.sweeptime = np.array([0])
            for iw in range(1, self.segments + 1):
                self.sweeptime = np.append(self.sweeptime, np.round(np.linspace((self.sweeptime[-1] + self.dE/self.sr), (iw*self.window/self.sr), self.dp, endpoint = True), decimals = 3))
            
            self.sweep = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.sweep = np.append(self.sweep, np.round(np.linspace(self.Eini + self.dE, self.Eupp, self.dp, endpoint = True), decimals = 4))
                self.sweep = np.append(self.sweep, np.round(np.linspace(self.Eupp - self.dE, self.Eini, self.dp, endpoint = True), decimals = 4))

            self.steptime = np.array([])
            for iy in range(0, self.sweeptime.size - 1):
                self.steptime = np.append(self.steptime, np.linspace(self.sweeptime[iy], self.sweeptime[iy + 1], self.sp))

            self.step = np.array([])
            for iz in range(0, self.segments * self.dp):
                self.step = np.append(self.step, np.round(np.linspace(self.sweep[iz], self.sweep[iz + 1], self.sp), decimals = 7))

        

        if self.Eini == self.Eupp:
            self.segments = 2 * self.ns          # Number of segments expected          
            self.window = self.Eupp - self.Elow         # Potential window of each segment
            self.dp = int(self.window/self.dE)       # Number of data points in each potential window
            
            self.sweeptime = np.array([0])
            for iw in range(1, self.segments + 1):
                self.sweeptime = np.append(self.sweeptime, np.round(np.linspace((self.sweeptime[-1] + self.dE/self.sr), (iw*self.window/self.sr), self.dp, endpoint = True), decimals = 3))
            
            self.sweep = np.array([self.Eini])
            for ix in range(0, self.ns):
                self.sweep = np.append(self.sweep, np.round(np.linspace(self.Eini + self.dE, self.Elow, self.dp, endpoint = True), decimals = 4))
                self.sweep = np.append(self.sweep, np.round(np.linspace(self.Elow - self.dE, self.Eini, self.dp, endpoint = True), decimals = 4))

        
            self.step = np.array([])
            for iz in range(0, self.segments * self.dp):
                try:
                    self.step = np.append(self.step, np.round(np.linspace(self.sweep[iz], self.sweep[iz + 1] - self.dE/self.sp, self.sp), decimals = 7))
                except:
                    self.step = np.append(self.step, np.round(np.linspace(self.sweep[iz], self.sweep[-1], self.sp + 1), decimals = 7))


        if self.Elow < self.Eini < self.Eupp:
            self.segments = 3 * self.ns          # Number of segments expected          
            self.uppwindow = self.Eupp - self.Eini         # Potential window of each segment
            self.window = self.Eupp - self.Elow
            self.lowwindow = self.Eini - self.Elow
            self.uppdp = int(self.uppwindow/self.dE)
            self.dp = int(self.window/self.dE)       # Number of data points in each potential window
            self.lowdp = int(self.lowwindow/self.dE)

            self.time = np.array([])
            for ix in range(0, self.ns):
                self.time = np.append(self.time, np.round(np.linspace(0, (self.window - self.dE)/self.sr, self.dp), decimals = 3))
                self.time = np.append(self.time, np.round(np.linspace(0, (self.window - self.dE)/self.sr, self.dp), decimals = 3))
                self.time = np.append(self.time, np.round(np.linspace(0, (self.window - self.dE)/self.sr, self.dp), decimals = 3))

            self.sweep = np.array([])
            for iy in range(0, self.ns):
                self.sweep = np.append(self.sweep, np.round(np.linspace(self.Eini, self.Eupp - self.dE, self.uppdp), decimals = 4))
                self.sweep = np.append(self.sweep, np.round(np.linspace(self.Eupp, self.Elow + self.dE, self.dp), decimals = 4))
                self.sweep = np.append(self.sweep, np.round(np.linspace(self.Elow, self.Eini - self.dE, self.lowdp), decimals = 4))
            



    def waveform(self):
        return self.sweep 


    def CV(self):
        '''Returns E vs. i for a CV performed on a capacitor with parameters derived from the Capacitance() class\n
        Uses equation 1.6.23 from the 3rd edition of Electrochemical Methods:\n
        i = sr*Cd*(1-np.exp(-t/(Ru*Cd)))'''
        
        if self.Eini == self.Elow:
            i = np.array([])
            for iy in range(0, self.ns):
                i = np.append(i, self.sr*self.Cd*(1-np.exp((-self.sweeptime[0 + self.dp*iy:self.dp*(1+iy)])/(self.Ru*self.Cd))))
                i = np.append(i, -self.sr*self.Cd*(1-np.exp((-self.sweeptime[0 + self.dp*iy:self.dp*(1+iy)])/(self.Ru*self.Cd))))
        return zip(self.sweep, i)
        

    def CSV(self):
        '''Returns E vs. i for a CSV performed on a capacitor with parameters derived from the Capacitance() class\n
        Uses equation 1.6.17 from the 3rd edition of Electrochemical Methods:\n
        i = (dE/Ru)*np.exp(-t/(Ru*Cd))'''
        
        if self.Eini == self.Elow:
            i = np.array([])
            for ix in range(0, self.segments):
                if ix % 2 == 0:
                    i_pos = np.array([0])
                    for iy in range(0, self.dp):
                        if iy == 0:
                            t = np.linspace(0, self.time[-1], self.dp*self.sp)
                            i_pos = np.append(i_pos, (self.dE/self.Ru)*np.exp((-t)/(self.Ru*self.Cd)))
                        else:
                            t = np.linspace(0, self.time[-(iy+1)], (self.dp - iy)*self.sp)
                            data = np.zeros(iy*self.sp + 1)
                            data = np.append(data, (self.dE/self.Ru)*np.exp((-t)/(self.Ru*self.Cd)))
                            i_pos = np.add(i_pos,data)
                    i = np.append(i, i_pos)

                elif ix % 2 != 0:
                    i_neg = np.array([0])
                    for iy in range(0, self.dp):
                        if iy == 0:
                            t = np.linspace(0, self.time[-1], self.dp*self.sp)
                            i_neg = np.append(i_neg, (-self.dE/self.Ru)*np.exp((-t)/(self.Ru*self.Cd)))
                        else:
                            t = np.linspace(0, self.time[-(iy+1)], (self.dp - iy)*self.sp)
                            data = np.zeros(iy*self.sp + 1)
                            data = np.append(data, (-self.dE/self.Ru)*np.exp((-t)/(self.Ru*self.Cd)))
                            i_neg = np.add(i_neg,data)
                    i = np.append(i, i_neg)
        return  i


if __name__ == '__main__':
    example = Capacitance(Eini=0,Elow=0, ns = 3)
    #linear = example.CV()
    #staircase = example.CSV()
    test = 'C:/Users/SLinf/Documents/data.txt'
    with open(test, 'w') as file:
        for ix in example.step:
            file.write(str(ix) + '\n')
    #test2 = 'C:/Users/SLinf/Documents/GitHub/oscilloscope-reader/CSV.txt'
    #with open(test2, 'w') as file:
        #for ix,iy in staircase:
            #file.write(str(ix) + ',' + str(iy) + '\n')
