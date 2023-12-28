import os
import numpy as np
import waveforms as wf

cwd = os.getcwd()
shape = wf.CyclicLinearVoltammetry(Eini = 0, Eupp = 0.5, Elow = 0, dE = 0.002, sr = 1, ns = 1, osf = 200000)

y = np.sin(2*np.pi*shape.t)
w1 = np.linspace(0,1, 8)
w = np.linspace(1,-1, 16)
w2 = np.linspace(-1, 0, 8)

find = np.array([])
for ix in w1:
    find = np.append(find, np.arcsin(ix) / (2 * np.pi))
for ix in w:
    find = np.append(find, 0.5 - (np.arcsin(ix) / (2 * np.pi)))
for ix in w2:
    find = np.append(find, 1 + (np.arcsin(ix) / (2 * np.pi)))

z = np.array([])
for ix in range(0, find.size):
    try:
        z = np.append(z, np.sin(2*np.pi*find[ix])*np.ones([int(np.where(shape.t > find[ix])[0][0]) - int(np.where(shape.t > find[ix - 1])[0][0])]))
    except: 
        pass
output = zip(shape.t, y, z)
'''7. SAVE THE DATA'''
with open(f'{cwd}/data/sin.txt', 'w') as file:
    for ix, iy, iz in output:
        file.write(str(ix) + ',' + str(iy) + ',' + str(iz) + '\n')