# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:34:01 2018

@author: mihainipomici
"""
import numpy as np
def roundGrade(grades):
    gradeScale = np.array([-3, 0, 2, 4, 7, 10, 12])
    for i in range(len(grades)):
        grades[i] = min(gradeScale, key = lambda x:abs(x - grades[i]))
    gradesRounded = grades.astype(int)
    return gradesRounded
    