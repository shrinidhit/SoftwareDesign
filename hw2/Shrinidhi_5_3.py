# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 00:21:41 2014

@author: shrinidhit
"""
#Function without user input
def check_fermat(a,b,c,n):
    #Checks if integer is less than 2
    if n <= 2:
        print "No, that doesn't work"
    #Checks Fermat's theorem
    elif (a**n + b**n) == c**n:
        print "Holy Smokes, Fermant was wrong!"
    else:
        print "No, that doesn't work"

#Function with user input
def check_fermat_input():
    #gets and converts user inputs for a, b, c, and n to ints
    a = int(raw_input('Enter your a value:'));
    b = int(raw_input('Enter your b value:'));
    c = int(raw_input('Enter your c value:'));
    n = int(raw_input('Enter your n value:'));
    #Checks Fermat's Theorem
    if n <= 2:
        print "No, that doesn't work"
    elif (a**n + b**n) == c**n:
        print "Holy Smokes, Fermant was wrong!"
    else:
        print "No, that doesn't work"
