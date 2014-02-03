# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 00:42:19 2014

@author: shrinidhit
"""
#Compares two values, x and y:
def compare_values(x,y):
    if x > y: #Checks and leaves function if x > y
        return 1
    elif x == y: #Checks and leaves function if x = y
        return 0
    else: #Only other option of x < y
        return -1