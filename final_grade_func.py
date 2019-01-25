# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:59:57 2018

@author: mihainipomici
"""

import numpy as np
from roundgrade_function import roundGrade

# computeFinalGrades FUNCTION - computes the average value on the 7-step-scale 
# of a vector that contains grades.
#
# Usage: gradesFinal = computeFinalGrades(grades)
#
# Input: grades - an N × M matrix containing grades on the 7-step-scale given to N students on M different assignments.
#
# Output: gradesFinal - a vector which contains only the final grades on the 7-step-scale
#
# Author: Mihai Nipomici

def computeFinalGrades(grades):
    M = np.size(grades,axis = 1)  # M - number of columns
    N = np.size(grades, axis = 0)  # N - number of rows
    gradesFinal = np.array([], dtype = int)  # this will eventually store the final grades
    for i in range(N):
        if M == 1:
            gradesFinal = np.append(gradesFinal, roundGrade([[grades[i]]]))
        elif M > 1:
            currentRow = grades[i,:] # a vector/current row from the matrix of N x M grades
            if -3 in currentRow:
                gradesFinal = np.append(gradesFinal, -3)
            else:
                currentRow = np.sort(currentRow) # the row is then sorted in ascending order
                currentRow = currentRow[1:len(currentRow)] # the first value is cut off the vector as it is the smallest one
                averageGrade = np.average(currentRow)
                finalGrade = roundGrade([averageGrade]) # the final grade is then rounded to the nearest 7-step-scale grade
                                                        # by using the roundGrade function
                gradesFinal = np.append(gradesFinal, finalGrade)
    return gradesFinal