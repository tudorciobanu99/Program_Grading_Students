# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:34:01 2018

@author: mihainipomici
"""
import numpy as np

# roundGrade FUNCTION - Rounds each element of a vector to the nearest
# grade on the 7-step-scale [-3,0,2,4,7,10,12].
#
# Usage: gradesRounded = roundGrade(grades)
#
# Input: grades - a vector which contains floats/integers in the range (-3,12)
#
# Output: gradesRounded - a vector which contains only the grades on the 7-step-scale
#
# Author: Mihai Nipomici

def roundGrade(grades):
    gradeScale = np.array([-3, 0, 2, 4, 7, 10, 12], dtype = int)
    gradesRounded = np.zeros(len(grades), dtype = int) # this will eventually store the rounded grades
    for i in range(len(grades)):
        # the min function with the following parameters will the return the minimum value from the gradeScale vector of the
        # function x:abs(x-grades[i])
        gradesRounded[i] = min(gradeScale, key = lambda x:abs(x - grades[i])) # lambda x:abs(x-grades[i]) is an inline function which
                                                                              # returns the absolute value of the difference between
                                                                              # x (values from gradeScale vector) and the current element
                                                                              # from the grades vector
    return gradesRounded
    