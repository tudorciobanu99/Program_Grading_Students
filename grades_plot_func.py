"""
Created on Mon Nov 12 11:34:01 2018

@author: tudorciobanu
"""

import matplotlib.pyplot as plt
import math
from final_grade_func import computeFinalGrades
from roundgrade_function import roundGrade
import numpy as np

# gradesPlot FUNCTION - displays two plots:
# 1. A bar plot of the number of students who have received each of possible final grades on the 7-step-scale.
# 2. A plot with the assignments on the x-axis and the grades on the y-axis.
# The x-axis shows all assignments, and the y-axis shows all grades from −3 to 12.
#
# Usage: gradesPlot(grades)
#
# Input: grades - an N × M matrix containing grades on the 7-step-scale given to N students on M different assignments.
#
# Output: None
#
# Screen output: Plots
#
# Author: Tudor Ciobanu

def gradesPlot(grades):
    
    # Final grades plot
    finalGrades = computeFinalGrades(grades) # an array that stores the final grades of M - assignments for each N - students
    gradeScale = np.array([-3, 0, 2, 4, 7, 10, 12]) # an array that stores the allowed 7-step-scale grades
    gradesAxis = np.array([]) # this will eventually store the grades for the X - axis of the plot
    finalGradesCounter = np.array([], dtype = int) # an array that stores the number of each grade on the 7-step-scale
    for i in range(len(gradeScale)):
        grade = np.where(finalGrades == gradeScale[i]) # an array that stores the indexes of the elements from the grades vector where
                                                       # each of the 7-step-scale grades are encountered
        if (len(finalGrades[grade]) > 0): # if no elements in the grades array are found for the 7-steps-scale grade, it is not included
                                          # in the plot
            finalGradesCounter = np.append(finalGradesCounter, len(finalGrades[grade])) # the number of encounters is then appended
            gradesAxis = np.append(gradesAxis, str(gradeScale[i])) # the 7-step-scale grade is then added to the X-axis
    width = 0.8
    if (len(gradesAxis) < 4): # if the X - axis has less than 4 grades, then the width of the columns is set to half
        width = 0.4
        
    ax1 = plt.subplot()
    ax1.bar(gradesAxis, finalGradesCounter, color = 'g', label = grades, width = width) # a bar plot with gradesAxis as the X-axis and
                                                                                        # finalGradesCounter as the Y-axis
    ax1.set_xticklabels(gradesAxis) # the values from the gradeAxis are set as the locations where the ticks should be placed
    yint = range(min(finalGradesCounter), math.ceil(max(finalGradesCounter))+1) # a range based on the nr of encounters of each grade
                                                                                # from the finalGradesCounter array
    plt.yticks(yint)
    plt.xlabel('Final grades')
    plt.ylabel('Number of final grades matching')
    plt.title('Final grades')
    plt.show()
    
    # Grades per assignment plot
    ax2 = plt.subplot()
    M = np.size(grades, axis = 1) # M - nr of columns of the grades matrix
    lineY = np.array([], dtype = int) # this will eventually store the y - coordinates of each average grade for each assignment
    lineX = np.arange(1,M+1) # this array stores the x - coordinates of each average grade for each assignment
    plt.xticks(np.arange(1,M+1, 1.0)) # the locations for the x-ticks are set to be from 1 to M
    plt.yticks(np.arange(-3, 13, 1.0)) # the locations for the y-ticks are set to be from -3 to 12
    plt.ylim(-4,13) # the limits for the Y-axis
    
    for i in range(M):
        yAxis = grades[:,i] # the Y - coordinates for each grade of each student i(i = 1..N)
        xAxis = np.repeat(i+1,len(yAxis)) # the X - coordinates for each grade of each student i(i = 1..N)
        lineY = np.append(lineY, np.average(yAxis)) 
        xAxisUpdated = np.array([]) # an array that stores the new X - shifted coordinates of each grade
        yAxisUpdated = np.array([]) # an array that stores the new Y - shifted coordinates of each grade
        for k in range(len(yAxis)):
            yAxisUpdated = np.append(yAxisUpdated, yAxis[k] + np.random.uniform(-0.1,0.1)) # a random number from -0.1 to 0.1 is added
                                                                                           # to current X-coordinate
            xAxisUpdated = np.append(xAxisUpdated, xAxis[k] + np.random.uniform(-0.1,0.1)) # a random number from -0.1 to 0.1 is added
                                                                                           # to current Y-coordinate
        ax2.scatter(xAxisUpdated,yAxisUpdated) # a scatter plot with xAxisUpdated as the X-axis and
                                               # yAxisUpdated as the Y-axis for each grades for the student
    
    ax2.plot(lineX,lineY, color = 'purple', label = 'Avg grade line') # a line that connects all the average grades for each assignment
    plt.xlabel('Assignments')
    plt.ylabel('Grades for the assignments')
    plt.title('Grades per assignment')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.) # this location code was copied from https://matplotlib.org/users/legend_guide.html
    plt.show()