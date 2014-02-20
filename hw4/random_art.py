# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014

@author: pruvolo and sthirumalai
"""
#importing for math calculations
from math import sin
from math import cos
from math import pi
#importing for random choosers
from random import randint
from random import choice
#importing for creating image
from PIL import Image

def build_random_function(min_depth, max_depth):
    '''
    Generates complex function nested an amount of times between min_depth 
    and max_depth. The function is made from a list of basic building blocks
    These building blocks are prod, cos_pi, sin_pi, x, y, square_single, and cube_double
    '''
    #creates list of basic function names
    single_unit_functions = ['cos_pi', 'sin_pi', 'square_single'] #functions requiring only one input
    double_unit_functions = ['prod', 'x', 'y', 'cube_double'] #functions requiring two inputs
    #base case:
    if max_depth == 1: #if maxdepth is reached, recursion stops
        return choice([['x'],['y']])
    elif min_depth == 1 and randint(0,2) == 0: #if mindepth is reached but not maxdepth, randomly decides if recursion should stop
        return choice([['x'],['y']])
    #if not base case:
    elif randint(0,2) == 0: #use single unit functions
        return [choice(single_unit_functions), build_random_function(min_depth-1, max_depth-1)]
    else: #use double unit functions
        return [choice(double_unit_functions), build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
    
def evaluate_random_function(f, x, y):
    '''
    Calcualtes value of a complex function in the form ['functionname',[xinput], [yinput]].
    The basic unit function names are prod, sin_pi, cos_pi, x, y, square_single, and cube_double
    This function returns the calculated value
    '''
    x = float(x) #converts x and y to float in case decimal was forgottin in input
    y = float(y)
    #base cases
    if f == ['x']:
        return x
    elif f == ['y']:
        return y
    #other cases
    elif f[0] == 'prod': #prod(a,b) = ab
        return (evaluate_random_function(f[1], x, y)) * (evaluate_random_function(f[2], x, y))
    elif f[0] == 'cos_pi':#cos_pi(a) = cos(pi*a)
        return cos(pi * evaluate_random_function(f[1], x, y))
    elif f[0] == 'sin_pi': #sin_pi(a) = sin(pi*a)
        return sin(pi * evaluate_random_function(f[1], x, y))
    elif f[0] == 'x': #x(a,b) = a
        return evaluate_random_function(f[1], x, y)
    elif f[0] == 'y': #y(a,b) = b
        return evaluate_random_function(f[2], x, y)
    elif f[0] == 'square_single': #square_single(a) = a^2
        return (evaluate_random_function(f[1], x, y))**2.0
    elif f[0] == 'cube_double': #cube_double(a,b) = a^3 + b^3
        return ((evaluate_random_function(f[1], x, y))**3.0)/2 + (evaluate_random_function(f[2], x, y)**3.0)/2
    else: #if no functions are recognized, returns error
        return "function not recognized"
   
def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
    """
    shift = output_interval_start #amount new value is shifted by
    scale = ((val - input_interval_start)/(input_interval_end - input_interval_start) * (output_interval_end - output_interval_start)) #amount new value is scaled by
    return shift + scale #final answer
    
def create_image():
    """ Generates an image from complex functions, then saves the image file
        1. Generate random functions for the red, green, and blue channels
        2. Creates an image by plotting each function's value in each x,y position.
           In this model, darkness of pixel corresponds to value
        3. Saves image
    """
    #Generate random functions for the red, green, and blue channels
    red_function = build_random_function(5, 10)
    green_function = build_random_function(5, 10)
    blue_function = build_random_function(5, 10)
    #Create an empty color image using PIL
    im = Image.new("RGB",(350,350)) #350 by 350 pixel image
    im2 = im.load()
    #Creating image for functions
    for xp in range(0, 350):
        for yp in range(0,350):
            #rescales x and y from -1 to positive 1
            x = remap_interval(float(xp), 0.0, 350.0, -1.0, 1.0)
            y = remap_interval(float(yp), 0.0, 350.0, -1.0, 1.0)
            #gets pixel values according to red, green, and blue functions
            red_val = int(remap_interval(evaluate_random_function(red_function, x, y), -1.0, 1.0, 0.0, 255.0))
            green_val = int(remap_interval(evaluate_random_function(green_function, x, y), -1.0, 1.0, 0.0, 255.0))
            blue_val = int(remap_interval(evaluate_random_function(blue_function, x, y), -1.0, 1.0, 0.0, 255.0))
            #sets pixel value
            im2[xp,yp]=(red_val, green_val, blue_val)
    #Save image
    im.save("test7.bmp")
    
    
    