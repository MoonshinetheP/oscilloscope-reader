import numpy as np
import simulations as sim

def interval(input, intervals):
    '''This function finds the position of each transient and the real interval time between each step'''
    '''It then uses this information to give an accurate account of the duration and position of each potential step'''
    
    absolute = np.abs(input)
    
    a = 0
    list_of_intervals = np.array([])

    while a < (absolute.size - intervals + 1):
        moving_window = absolute[a : a + intervals]
        peak = np.argmax(moving_window)
        list_of_intervals = np.append(list_of_intervals, int(peak) + a + 1)
        a += intervals
    
    diff_of_intervals = np.diff(np.array(list_of_intervals))
        
    minimum_interval = np.amin(list_of_intervals)

    return (list_of_intervals, diff_of_intervals, minimum_interval)


def raw(input):
    '''Currently returns the oscilloscope data in its raw form'''
    raw_save = 'raw.txt'
    with open(filepath + raw_save,'w') as file:
        for x in input:
            file.write(str(x) + '\n')


def MA(input, window = 500, step = 1):
    '''Returns the moving average of the oscilloscope data in the form of voltage (detailed) vs. averaged current''' 
    i = 0
    MA_list = np.array([])
    while i < input.size - window + 1:
        MA_window = input[i : i + window]
        window_average = np.sum(MA_window) / window
        MA_list = np.append(MA_list, window_average)
        i += step

    with open(filepath + 'MA.txt','w') as file:
        for ix in MA_list:
            file.write(str(ix) + '\n')
    

def CA(input, intervals, alpha = 0.5):
    '''Returns the current average of each potential step in the oscilloscope data in the form of voltage (simplified) vs. averaged current'''

    CA_data = interval(input, intervals)[0]

    CA_list = np.array([])
    if alpha > 1 or alpha < 0.005:
        pass
    else:
        for x in range(0, CA_data.size):
            try:
                data = input[int(CA_data[x]):int(CA_data[x+1])]
            except:
                data = input[int(CA_data[x]):] 
            period = alpha*(data.size)                                                    
            sampled = np.sum(data[-int(period):]) / period   
            CA_list = np.append(CA_list, sampled)
    
    CA_save = f'CA{alpha}.txt'
    with open(filepath + CA_save,'w') as file:
        for ix in list(CA_list):
            file.write(str(ix) + '\n')


if __name__ == '__main__':
    filepath = 'C:/Users/SLinf/Documents/GitHub/oscilloscope-reader/'
    example = sim.Capacitance(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.002 , sr = 0.2, ns = 1, Cd = 0.000050, Ru = 500, sp = 1000)
    staircase = example.CSV()
    raw(staircase)
    MA(staircase, 1000, 1)
    CA(staircase, 1000, 0.25)
    CA(staircase, 1000, 0.5)
    CA(staircase, 1000, 0.75)
    CA(staircase, 1000, 0.95)
    '''response = interval(staircase, int(example.sp), 0.5)
    current_save = 'current.txt'
    with open(filepath + current_save, 'w') as file:
        for x in response[1]:
            file.write(str(x) + '\n')'''