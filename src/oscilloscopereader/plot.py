import sys
import os
from errno import EEXIST
import time

import numpy as np
import matplotlib.pyplot as plt

import waveforms as wf
import simulations as sim


if __name__ == '__main__':
    
    cwd = os.getcwd()

    try:
        os.makedirs(cwd + '/data')
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(cwd + '/data'):
            pass
        else: 
            raise
    
    try:
        os.makedirs(cwd + '/plots')
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(cwd + '/plots'):
            pass
        else: 
            raise
    

    '''SIMULATION'''
    start = time.time()

    #shape = wf.CV(Eini = 0.25, Eupp = 0.5, Elow = 0, dE = -0.005, sr = 0.1, ns = 1)
    shape = wf.CSV(Eini = 0.5, Eupp = 0.5, Elow = 0, dE = -0.001, sr = 0.1, ns = 1, st = 0.001, detailed = True)

    instance = sim.Capacitance(input = shape, Cd = 0.000050, Ru = 500)
    
    end = time.time()
    print(f'The simulation took {end-start} seconds to complete')


    '''PLOT GENERATION'''
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12, 5))
    left, = ax1.plot(shape.tWF, shape.EWF, linewidth = 1, linestyle = '-', color = 'blue', marker = None, label = None, visible = True)
    if shape.detailed == True:
        right, = ax2.plot(shape.EPLOT[shape.sp:], instance.i, linewidth = 1, linestyle = '-', color = 'red', marker = None, label = None, visible = True)
    elif shape.detailed == False:
        print('\n' + 'Cannot currently plot simplified CSV waveforms, try usng CV instead' + '\n')
        sys.exit()
    else:
        right, = ax2.plot(shape.EPLOT[1:], instance.i, linewidth = 1, linestyle = '-', color = 'red', marker = None, label = None, visible = True)


    '''PLOT SETTINGS'''
    ax1.set_xlim(np.amin(shape.tWF) - (0.1 * (np.amax(shape.tWF) - np.amin(shape.tWF))), np.amax(shape.tWF) + (0.1 * (np.amax(shape.tWF) - np.amin(shape.tWF))))
    ax1.set_ylim(np.amin(shape.EWF) - (0.1 * (np.amax(shape.EWF) - np.amin(shape.EWF))), np.amax(shape.EWF) + (0.1 * (np.amax(shape.EWF) - np.amin(shape.EWF))))
    ax1.set_title('E vs. t', pad = 15, fontsize = 20)
    ax1.set_xlabel('t / s', labelpad = 5, fontsize = 15)
    ax1.set_ylabel('E / V', labelpad = 5, fontsize = 15)

    ax2.set_xlim(np.amin(shape.EPLOT) - (0.1 * (np.amax(shape.EPLOT) - np.amin(shape.EPLOT))), np.amax(shape.EPLOT) + (0.1 * (np.amax(shape.EPLOT) - np.amin(shape.EPLOT))))
    ax2.set_ylim(np.amin(instance.i) - (0.1 * (np.amax(instance.i) - np.amin(instance.i))), np.amax(instance.i) + (0.1 * (np.amax(instance.i) - np.amin(instance.i))))
    ax2.set_title('i vs. E', pad = 15, fontsize = 20)
    ax2.set_xlabel('E / V', labelpad = 5, fontsize = 15)
    ax2.set_ylabel('i / A', labelpad = 5, fontsize = 15)

    plt.show()
    plt.close()