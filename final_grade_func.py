# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:59:57 2018

@author: mihainipomici
"""

import numpy as np
from roundgrade_function import roundGrade

def computeFinalGrades(grades):
    N = np.size(grades,axis = 1)
    M = np.size(grades, axis = 0)
    gradesFinal = np.array([], dtype = int)
    for i in range(N):
        if M == 1:
            gradesFinal = np.append(gradesFinal, roundGrade(grades[i]))
        elif M > 1:
            currentRow = grades[i,:]
            if -3 in currentRow:
                gradesFinal = np.append(gradesFinal, -3)
                break
            else:
                currentRow = np.sort(currentRow)
                averageGrade = np.average(currentRow)
                finalGrade = roundGrade(np.array([averageGrade]))
                gradesFinal = np.append(gradesFinal, finalGrade)
    return gradesFinal






