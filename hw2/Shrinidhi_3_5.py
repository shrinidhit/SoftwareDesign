# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: shrinidhit
"""
#Draws grid for specified number of rows and columns
def grid(row, col):
    #Basic Unit Creation
    linebreakunit = (' _' * 4) + ' +'; #basic repeating unit within grid lines
    midlineunit = ('  ' * 4) + ' |'; #basic repeating unit within mid lines
    #Basic Row Creation
    linebreakrow = '+' + (linebreakunit * col); #creates row for grid lines
    midrow = '|' + (midlineunit * col); #created row for all other mid lines
    #Prints Grid
    for x in range(0, row): #Unit of multiple rows repeated in grid
        print linebreakrow
        print midrow
        print midrow
        print midrow
        print midrow
    print linebreakrow #closes off grid with one last linebreak row

    
    