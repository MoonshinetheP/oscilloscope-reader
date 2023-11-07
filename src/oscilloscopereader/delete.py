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

Filename:           delete.py

===================================================================================================

Description:

This file contains additional code which can be used to empty the /data, /analysis, and /plots 
folders with any files and images that were generated during the use of the other files in the 
oscilloscope-reader package.
 
===================================================================================================

How to use this file:
    
In order to use this file:
    1. Scroll down the the bottom of the file, to the 'DELETING DATA FROM MAIN' section.
    2. In the instance of the Eraser class, change the Boolean operator for the folders you want
       to empty to True
    3. Run the python file

===================================================================================================
'''


import os


class Eraser:

    '''Deletes all items from the selected folders \n
    
    Requires: \n
    data - a True or False option for whether items in the /data folder are deleted or not \n
    analysis - a True or False option for whether items in the /analysis folder are deleted or not \n
    plots - a True or False option for whether items in the /plots folder are deleted or not'''

    def __init__(self, data = False, analysis = False, plots = False):
        
        self.data = [data, '/data']     # initialised parameter with the data Boolean and the corresponding /data directory string
        self.analysis = [analysis, '/analysis']     # initialised parameter with the analysis Boolean and the corresponding /analysis directory string
        self.plots = [plots, '/plots']      # initialised parameter with the plots Boolean and the corresponding /plots directory string
        
        cwd = os.getcwd()       # finds the current working directory

        for ix in (self.data, self.analysis, self.plots):       # loops through all intialised parameters
            if ix[0] == True:       # checks whether the first part of the parameter is True
                try:
                    for iy in os.listdir(cwd + ix[1]):      # if so, loops through all files in the directory corresponding to that parameter
                        os.remove(cwd + ix[1] + '/' + iy)       # and removes it
                except:
                    raise       # raises an error just in case something gets in the way


"""
===================================================================================================
DELETING DATA FROM MAIN
===================================================================================================
"""

if __name__ == '__main__':

    Eraser(data = True, analysis = True, plots = True)