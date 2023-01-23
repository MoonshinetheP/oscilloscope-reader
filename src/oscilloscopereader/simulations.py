import sys
import numpy as np

class Capacitance:
    '''Simulates the charging of a double layer when using CV or CSV \n 
    Also takes input parameters and uses them to create potential waveforms for CV and CSV'''
    def __init__(self, Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.002 , sr = 0.2, ns = 1, Cd = 0.000050, Ru = 500, sp = 1000):
        
        self.Eini = Eini        # Start potential
        self.Eupp = Eupp        # Upper vertex potential
        self.Elow = Elow        # Lower vertex potential
        self.dE = dE        # Step size
        self.sr = sr        # Scan rate
        self.ns = ns        # Number of scans
        self.Cd = Cd        # Double layer capacitance
        self.Ru = Ru        # Uncompensated resistance
        self.sp = sp        # Number of points in a step


        if self.Eini == self.Elow and self.dE > 0:          
            self.segments = 2 * self.ns          # Number of segments expected          
            self.window = self.Eupp - self.Eini         # Potential window of each segment
            self.dp = int(self.window/self.dE)       # Number of data points in each potential window
            
            self.time = np.array([])
            for ix in range(0, self.segments):
                self.time = np.append(self.time, np.round(np.linspace(0, (self.window - self.dE)/self.sr, self.dp), decimals = 3))
            
            self.sweep = np.array([])
            for iy in range(0, self.ns):
                self.sweep = np.append(self.sweep, np.round(np.linspace(self.Eini, self.Eupp - self.dE, self.dp), decimals = 4))
                self.sweep = np.append(self.sweep, np.round(np.linspace(self.Eupp, self.Eini + self.dE, self.dp), decimals = 4))
        
            self.step = np.array([])
            for iz in range(0, self.segments * self.dp):
                try:
                    self.step = np.append(self.step, np.round(np.linspace(self.sweep[iz], self.sweep[iz + 1] - self.dE/self.sp, self.sp), decimals = 7))
                except:
                    self.step = np.append(self.step, np.round(np.linspace(self.sweep[iz], self.sweep[-1], self.sp + 1), decimals = 7))
        

        if self.Eini == self.Eupp and self.dE < 0:
            pass


        if self.Eini > self.Elow and self.Eini < Eupp:
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
            

        '''Errors'''
        if self.Eini < self.Elow:
            print('\n' + 'Initial potential must be higher than the lower vertex potential' + '\n')
            sys.exit()
        if self.Eini > self.Eupp:
            print('\n' + 'Initial potential must be lower than the upper vertex potential' + '\n')
            sys.exit()
        if self.Eini == self.Elow and self.dE < 0:
            print('\n' + 'Step potential must be positive for a positive scan direction' + '\n')
            sys.exit()
        if self.Eini == self.Eupp and self.dE > 0:
            print('\n' + 'Step potential must be negative for a negative scan direction' + '\n')
            sys.exit()

    def temp(self):
        return self.sweep 


    def CV(self):
        '''Returns E vs. i for a CV performed on a capacitor with parameters derived from the Capacitance() class\n
        Uses equation 1.6.23 from the 3rd edition of Electrochemical Methods:\n
        i = sr*Cd*(1-np.exp(-t/(Ru*Cd)))'''
        if self.Eini == self.Elow:
            i = np.array([])
            for iy in range(0, self.ns):
                i = np.append(i, self.sr*self.Cd*(1-np.exp((-self.time[0 + self.dp*iy:self.dp*(1+iy)])/(self.Ru*self.Cd))))
                i = np.append(i, -self.sr*self.Cd*(1-np.exp((-self.time[0 + self.dp*iy:self.dp*(1+iy)])/(self.Ru*self.Cd))))
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
    example = Capacitance(Eini=-0.2,Eupp=0.6,Elow=-1.4, dE= 0.01834862385, sr=0.1, ns=1)
    #linear = example.CV()
    #staircase = example.CSV()
    test = 'C:/Users/SLinf/Documents/CV.txt'
    with open(test, 'w') as file:
        for ix in example.temp():
            file.write(str(ix) + '\n')
    #test2 = 'C:/Users/SLinf/Documents/GitHub/oscilloscope-reader/CSV.txt'
    #with open(test2, 'w') as file:
        #for ix,iy in staircase:
            #file.write(str(ix) + ',' + str(iy) + '\n')
