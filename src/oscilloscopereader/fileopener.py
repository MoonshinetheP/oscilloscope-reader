import pandas as pd
import errno

class Oscilloscope:
    '''A class which opens an oscilloscope .csv file and converts it into a usable numpy array'''
    def __init__(self,file):
        df = pd.read_csv(file, header = 1, low_memory = False)
        self.array = df.to_numpy().astype(float)[:,1]

if __name__ == '__main__':
    path = 'C:/Users/SLinf/Documents/GitHub/oscilloscope-reader/'
    file = 'Newfile15.csv'
    test = Oscilloscope(path + file)