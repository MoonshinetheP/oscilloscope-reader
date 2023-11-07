'''
===================================================================================================
Copyright (C) 2023 Steven Linfield

This file is part of the oscilloscope-reader package. This package is free software: you can 
redistribute it and/or modify it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or (at your option) any later 
version. This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
GNU General Public License for more details. You should have received a copy of the GNU General 
Public License along with oscilloscope-reader. If not, see https://www.gnu.org/licenses/
===================================================================================================

Package title:      oscilloscope-reader
Repository:         https://github.com/MoonshinetheP/oscilloscope-reader
Date of creation:   22/10/2022
Main author:        Steven Linfield (MoonshinetheP)
Collaborators:      None
Acknowledgements:   None

Filename:           fileopener.py

===================================================================================================

Description:

This file contains the code used by the oscilloscope-reader package to open single oscilloscope 
files with .csv formats and to append the content of these files into numpy arrays which can then
be analysed and/or plotted. 

===================================================================================================

How to use this file:
    
This file has no standalone operational capabilities.

===================================================================================================
'''


import sys
import pandas as pd


class Oscilloscope:
    
    '''Opens a single oscilloscope file with a .csv format and converts it into a usable numpy array\n

    Requires:\n
    file - directory location of the oscilloscope data selected for analysis\n
    cf - user-defined voltage-to-current conversion factor of the potentiostat
    '''

    def __init__(self, file, cf):

        '''PARAMETER INITIALISATION'''
        self.label = 'imported'      # label for use in operations.py

        self.file = file        # location of the oscilloscope file which has been selected for analysis
        self.cf = cf        # conversion factor of voltage-to-current defined by the user for the potentiostat/settings used

        '''DATATYPE ERRORS'''
        if isinstance(self.cf, (float)) is False:       # checks that the conversion factor is a float value
            print('\n' + 'An invalid datatype was used for the conversion factor. Enter a float value.' + '\n')
            sys.exit()
        
        '''DATA VALUE ERRORS'''
        if self.cf <= 0:        # checks that the conversion factor is a positive non-zero value
            print('\n' + 'Conversion factor must be a postive non-zero value.' + '\n')
            sys.exit()

        '''OSCILLOSCOPE FILE IMPORT'''
        try:
            df = pd.read_csv(self.file, header = 1, low_memory = False)     # opens the .csv oscilloscope file into a pandas dataframe without the header and with full detail
            self.i = df.to_numpy().astype(float)[:,1]       # converts the pandas dataframe to a numpy filled with float values
            self.i *= -self.cf      # modifies the array using the conversion factor
        except:
            raise       # raises an error if the .csv file was not readable for any reason