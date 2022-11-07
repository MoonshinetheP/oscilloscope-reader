import numpy as np

class charging:
    '''Simulates charging of a double layer'''
    def __init__(self, Eini = 0, Eupp = 0.5, Elow = -0.5, dE = 0.001 , sr = 0.5, ns = 1, Cd = 0.000010, Ru = 5000):
        
        self.Eini = Eini
        self.Eupp = Eupp
        self.Elow = Elow
        self.dE = dE
        self.sr = sr
        self.ns = ns
        self.Cd = Cd
        self.Ru = Ru
            
        window = abs(self.Eupp-self.Elow)
        self.dp = int(window/self.dE)
        self.dpupp = int(((self.Eupp - self.Eini)/window)*self.dp)
        self.dplow = int(((self.Eini - self.Elow)/window)*self.dp)
        st = 1000
            
        self.sweeptime = np.linspace(0, (2*ns*window / sr), 2*ns*self.dp)
        self.steptime = np.linspace(0, (2*ns*window / sr), 2*ns*self.dp*st)
        
        self.sweep = np.array([])        
        self.sweep = np.append(self.sweep, np.linspace(self.Eini, self.Eupp, self.dpupp))
        self.sweep = np.append(self.sweep, np.linspace(self.Eupp, self.Elow, self.dp))
        self.sweep = np.append(self.sweep, np.linspace(self.Elow, self.Eini, self.dplow))

        self.step = np.array([])
        for iy in self.sweep:
            self.step = np.append(self.step, (np.ones([st])*iy))

        self.sweepdata = zip(self.sweeptime, self.sweep)
        self.stepdata = zip(self.steptime, self.step)
            

    def box(self, t):
        i = np.array([])
        for ix in t:
            if i.size < self.dpupp: 
                i = np.append(i, self.sr*self.Cd*(1-np.exp((-ix)/(self.Ru*self.Cd))))
            elif self.dpupp <= i.size < (self.dpupp + self.dp): 
                i = np.append(i, -1*self.sr*self.Cd*(1-np.exp((-ix + (ix-1))/(self.Ru*self.Cd))))
            elif (self.dpupp + self.dp) <= i.size < (2 * self.dp): 
                i = np.append(i, self.sr*self.Cd*(1-np.exp((-ix)/(self.Ru*self.Cd))))
        return zip(t,i)
        
    def spikes(self,t):
        return (-self.dE / self.Ru)*np.exp(-t / (self.Ru*self.Cd))

if __name__ == '__main__':
    cv = charging()
    data = cv.box(cv.sweeptime)
    test = 'C:/Users/SLinf/Documents/GitHub/oscilloscope-reader/test.txt'
    with open(test, 'w') as file:
        for ix,iy in data:
            file.write(str(ix) + ',' + str(iy) + '\n')
