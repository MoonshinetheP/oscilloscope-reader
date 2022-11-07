import numpy as np

def interval():
    '''This function finds the position of each transient and the real interval time between each step'''
    '''It then uses this information to give an accurate account of the duration and position of each potential step'''
    
    absolute = np.absolute(array_of_currents)
    
    peak_position = []
    a = 0
    
    while a < (absolute.size - interval_memory + 1):
        moving_window = absolute[a : a + interval_memory]
        peak = np.argmax(moving_window)
        peak_position.append(int(peak) + a + 1)
        a += interval_memory
    
    
    intervals = np.diff(np.array(peak_position))
    
    
    for z in intervals:  
        
        if z < (peakfinding_factor*np.sum(intervals))/(np.size(intervals)):
            index_of_mistake = np.where(intervals == z)
            intervals = np.delete(intervals, index_of_mistake[0][0])
        else:
            pass

    
    minimum_interval = np.amin(intervals)   # test this to see what minimum interval actually is
    #works up to here
    list_of_intervals = []
    b = 0
    
    while b < (absolute.size - minimum_interval + 1):
        recalculated_window = absolute[b : b + minimum_interval]
        peak_recount = np.argmax(recalculated_window)
        list_of_intervals.append(int(peak_recount)+ b + 1)
        b += minimum_interval
    
    diff_of_intervals = np.diff(np.array(list_of_intervals))
    for w in diff_of_intervals:
        if w <(peakfinding_factor * minimum_interval):
            index_of_second_mistake = np.where(diff_of_intervals == w)
            list_of_intervals = np.delete(list_of_intervals, index_of_second_mistake[0][0])
            diff_of_intervals = np.delete(diff_of_intervals, index_of_second_mistake[0][0])
        else:
            pass
        
    return (minimum_interval,list_of_intervals,diff_of_intervals)                 # to test, can I do a third run to improve peak differentials

   
def vertices():
    '''This function first finds the peak height of each transient in the absolute of the current data. Then, it reports at which data point this transient starts.'''

    vertex_window = interval_memory # For some reason, this interval memory is more accurate than calculated memory
    
    vertex_heights = []
    vertex_positions = []
    j = 0

    while j < len(list_of_currents) - vertex_window + 1:
        search_window = list_of_currents[j : j + vertex_window]
        minimum_vertex = min(search_window)         # maybe max would identify better
        vertex_heights.append(minimum_vertex)
        position = search_window.index(minimum_vertex)
        vertex_positions.append(position + j + 1)     
        j += int(vertex_window)
    
    '''This part of the function finds the difference between two adjacent current data points, then determines if it passes the threshold for a vertex'''
    upper_vertex = []
    lower_vertex = []
    diff = np.diff(vertex_heights)
    for x in diff:
        if x >= 0.5:
            spike = np.where(diff == x)
            lower_vertex_value = spike[0][0]
            lower_vertex.append(lower_vertex_value)
            print('Lower vertex is at ' + str(int(lower_vertex_value)))
        elif x <= -0.5:
            spike = np.where(diff == x)
            upper_vertex_value = spike[0][0]                                # Gives vertex position from 0
            upper_vertex.append(upper_vertex_value)
            print('Upper vertex is at ' + str(int(upper_vertex_value)))
        else:
            pass
    return (upper_vertex, lower_vertex)

def simplified():
    '''Uses the values found in the vertices() function to make a simplified voltage waveform (i.e. each step size)'''
    
    upper_vertex = vertices()[0][0]
    lower_vertex = vertices()[1][0] 
    start_point = (upper - (upper_vertex * step))
    
    print(start_point, upper, lower)
    simplified_waveform = []
    x  = len(simplified_waveform)
    for x in range(600):
        if x < upper_vertex:
            simplified_waveform.append(start_point + x * step)
        if x > upper_vertex and x < lower_vertex:
            simplified_waveform.append(upper - (x -upper_vertex) * step)
        if x > lower_vertex:
            simplified_waveform.append(lower + (x - lower_vertex) * step)        

    return simplified_waveform


def detailed():
    upper_vertex = vertices()[0][0]
    lower_vertex = vertices()[1][0] 
    start_point = (upper - (upper_vertex * step))    
    
    detailed_waveform = np.array([])
    list_of_intervals = interval()[2]
    
    for x in range(upper_vertex):
        detailed_waveform = np.append(detailed_waveform, np.linspace((start_point + x * step), (start_point + (x + 1) * step), list_of_intervals[x]))

    for x in range(upper_vertex, lower_vertex):
        detailed_waveform = np.append(detailed_waveform, np.linspace((upper - (x - upper_vertex) * step), (upper - ((x + 1) - upper_vertex) * step), list_of_intervals[x]))
        
    for x in range(lower_vertex, len(list_of_intervals)):
        detailed_waveform = np.append(detailed_waveform, np.linspace((lower + (x - lower_vertex) * step), (lower + ((x + 1) - lower_vertex) * step), list_of_intervals[x]))
       
    return detailed_waveform


def raw():
    '''Returns the raw oscilloscope data in the form of voltage (detailed) vs. current'''
    
    raw_zipped = zip(detailed(),list_of_currents)
    raw_save = ' raw.txt'
    with open(filepath + raw_save,'w') as file:
        for x,y in list(raw_zipped):
            file.write(str(x) + ',' + str(y) + '\n')


def MA(window_size = 500):
    '''Returns the moving average of the oscilloscope data in the form of voltage (detailed) vs. averaged current''' 
    
    i = 0
    MA_list = []
    while i < len(list_of_currents) - window_size + 1:
        MA_window = list_of_currents[i : i + window_size]
        window_average = sum(MA_window) / window_size
        MA_list.append(window_average)
        i += 1
    
    MA_zipped = zip(detailed(), MA_list)
    MA_save = ' MA.txt'
    with open(filepath + MA_save,'w') as file:
        for x,y in list(MA_zipped):
            file.write(str(x) + ',' + str(y) + '\n')
    

def CA(alpha = 0.5):
    '''Returns the current average of each potential step in the oscilloscope data in the form of voltage (simplified) vs. averaged current'''
    
    interval_pos = interval()[1]
    interval_wid = interval()[2]
    CA_data = []
    if alpha > 1 or alpha < 0.005:
        pass
    else:
        for x in range(len(interval_pos)-1):
            data = list_of_currents[interval_pos[x]:interval_pos[x] + interval_wid[x] +1]
            period = round(alpha*interval_wid[x])                                                      # Doesn't seem to work for low alpha
            sampled = data[int(interval_wid[x]) - int(period):int(interval_wid[x]) + 1]   # +1 does NOT WORK

            average = sum(sampled)/len(sampled)
            CA_data.append(average)
    
    CA_zipped = zip(simplified(), CA_data)
    CA_save = ' CA0.01.txt'
    with open(filepath + CA_save,'w') as file:
        for x,y in list(CA_zipped):
            file.write(str(x) + ',' + str(y) + '\n')

def publish_intervals():
    interval_positions = interval()[1]
    interval_memory = interval()[2]

    zipped_published = zip(interval_positions, interval_memory)
    zipped_save = 'intervals.txt'
    with open(filepath + zipped_save, 'w') as file:
        for x,y in list(zipped_published):
            file.write(str(x) + ',' + str(y) + '\n')