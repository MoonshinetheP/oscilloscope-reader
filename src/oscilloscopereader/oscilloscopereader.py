import pandas as pd
import numpy as np
import fileopener as fo
import simulations as sim
import operations as op
import plotting as plt


'''USER FILES'''
filepath = 'C:/Users/SLinf/Documents/GitHub/oscilloscope-reader/'
current = filepath + 'Newfile15.csv'

'''USER DEFINED PARAMETERS'''
upper = 1.3                                             # Upper vertex potential of the voltammogram (user-defined)
lower = -0.2                                            # Lower vertex potential of the voltammogram (user-defined)
scan = 0.5                                              # Scan rate (user-defined)
step = 0.005                                            # Step size (user-defined)
sample_rate = 1000000                                   # Sampling rate of the oscilloscope (user-defined)
peakfinding_factor = 0.5

'''CALCULATED PARAMETERS'''
interval = step/scan                                    # Theoretical interval time
interval_memory = int(interval * sample_rate)
graduations = step / interval_memory
experiment_time = 2 * (upper - lower) / scan
total_dp = int(experiment_time * sample_rate)



if __name__ == '__main__':
    data = fo.Oscilloscope(current)

    current_save = 'current.txt'
    with open(filepath + current_save, 'w') as file:
        for x in data.array:
            file.write(str(x) + '\n')