import matplotlib.pyplot as plt
import math
from final_grade_func import computeFinalGrades
from roundgrade_function import roundGrade
import numpy as np

def gradesPlot(grades):
    # Final grades
    finalGrades = computeFinalGrades(grades)
    gradeScale = np.array([-3, 0, 2, 4, 7, 10, 12])
    gradesAxis = np.array([])
    finalGradesCounter = np.array([], dtype = int)
    for i in range(len(gradeScale)):
        grade = np.where(finalGrades == gradeScale[i])
        if (len(finalGrades[grade]) > 0):
            finalGradesCounter = np.append(finalGradesCounter, len(finalGrades[grade]))
            gradesAxis = np.append(gradesAxis, str(gradeScale[i]))
    ax1 = plt.subplot()
    ax1.bar(gradesAxis, finalGradesCounter, color = 'g', label = grades)
    ax1.set_xticklabels(gradesAxis)
    yint = range(min(finalGradesCounter), math.ceil(max(finalGradesCounter))+1)
    plt.yticks(yint)
    plt.xlabel('Final grades')
    plt.ylabel('Number of final grades matching')
    plt.title('Final grades')
    plt.show()
    
    # Grades per assignment
    ax2 = plt.subplot()
    M = np.size(grades, axis = 1)
    lineY = np.array([], dtype = int)
    lineX = np.arange(1,M+1)
    for i in range(M):
        yAxis = grades[:,i]
        xAxis = np.repeat(i+1,len(yAxis))
        lineY = np.append(lineY, roundGrade(np.array([np.average(yAxis)])))
        xAxisUpdated = np.array([])
        yAxisUpdated = np.array([])
        for k in range(len(yAxis)):
            yAxisUpdated = np.append(yAxisUpdated, yAxis[k] + np.random.uniform(-0.1,0.1))
            xAxisUpdated = np.append(xAxisUpdated, xAxis[k] + np.random.uniform(-0.1,0.1))
        ax2.scatter(xAxisUpdated,yAxisUpdated)
        plt.xticks(np.arange(1,M+1, 1.0))
        plt.yticks(np.arange(-3, 13, 1.0))
        plt.ylim(-4,13)
    ax2.plot(lineX,lineY, color = 'purple', label = 'Avg grade line')
    plt.xlabel('Assignments')
    plt.ylabel('Grades for the assignments')
    plt.title('Grades per assignment')
    plt.legend()
    plt.show()
    
c = np.array([[7,4,-3,10],[12,12,12,-3],[7,2,2,2]])
gradesPlot(c)