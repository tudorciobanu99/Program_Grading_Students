#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 21:11:45 2018

@author: ciobanutudor
"""

import numpy as np
from roundgrade_function import roundGrade
from final_grade_func import computeFinalGrades
from grades_plot_func import gradesPlot
import pandas as pd

gradeScale = np.array([-3, 0, 2, 4, 7, 10, 12]) # an array which contains all the grades on the 7-step-scale
dataLoaded = False # a boolean variable that specifies if data has been loaded or not
fullData = None # a matrix N x M which stores that will eventually store the data loaded from the file
errorRows = np.array([], dtype = int) # an array that will eventually store the erroreous rows from the data
grades = np.array([]) # an array that will eventually store the positions in which the grades are not on the 7-step-scale



WARNING = '\033[93m' # changes font color to yellow
OK = '\033[92m' # changes font color to green
BACK = '\033[0m' # changes font color to normal
FAIL = '\033[31m' # changes font color to red



# is_number FUNCTION - checks if a string expression can be parsed as a number,
# either as a integer or float.
#
# Usage: is_number(expression, "int")
#
# Input: number - a string expression
#        kind - either "int" for integer or "float" for floats
#
# Output: True if the string can be parsed as the specified type of number or False if the condition is not met
#
# Author: Tudor Ciobanu
# Also used in Project 1

def is_number(s, kind):
    try:
        if (kind == "int"):
            int(s)
        elif (kind == "float"):
            float(s)
        return True
    except ValueError:
        return False
    

# printMenu FUNCTION - prints the main menu, registers the keyboard input and returns it
#
# Usage: choice = printMenu()
#
# Output: choice - a string that represents the keyboard input
#
# Author: Mihai Nipomici

def printMenu():
    print('\nMenu:')
    print('1. Load new data.')
    print('2. Check for data errors.')
    print('3. Generate plots.')
    print('4. Display list of grades.')
    print('5. Delete erroreous records.')
    print('6. Correct erroreous grades.')
    print('7. Quit.')
    choice = input('Please type in the number of the operation you would like to perform:  ')
    return choice


# loadStudents FUNCTION - loads data from a csv file and stores it in a N x M matrix
#
# Usage: fullData = loadStudents(filename)
#
# Input: filename - the name of the csv file
#
# Output: data - a N x M matrix with all the data from the csv file
#
# Author: Mihai Nipomici


def loadStudents(filename):
    data = np.array([]) # N x M matrix that will eventually store the data from the csv file
    try:
        data = pd.read_csv(filename) # the file is read
        data = np.array(data) # the data is loaded in a matrix
        M = np.size(data, axis = 1)-2  # M - number of assigment
        N = np.size(data, axis = 0)  # N - number of students
        print(OK + "\nFile " + filename + " has been loaded!" + BACK)
        print("Number of students: " + str(N))
        print("Number of assignments: " + str(M))
    except IOError:
        print(WARNING + "\nUnable to open the file with the following name: " + filename 
              + "! Please try again with a different filename! " + BACK)
    return data


# lcheckForDuplicateErrors FUNCTION - checks if a N x M matrix contains erroreous rows,
# specifically duplication errors and returns the indices for them.
#
# Usage: errorRows = checkForDuplicateErrors(data)
#
# Input: data - a N x M matrix
#
# Output: errorRows - an array with the indices for the erroreous rows/an empty array if no errors are found
#
# Author: Tudor Ciobanu

def checkForDuplicateErrors(data):
    N = np.size(data, axis = 0)  # N - number of students
    disregardedValues = np.array([]) # indices of the erroreous rows that have already been checked
    errors = False # True if errors have been found and False otherwise
    errorRows = np.array([], dtype = int) # indices of the erroreous rows
    print(WARNING + "\nDuplication errors in the data set: " + BACK)
    for i in range(N):
        currentStudent1 = data[i,:]
        for j in range(N):
            currentStudent2 = data[j,:]
            if (i != j and currentStudent1[0] == currentStudent2[0] and (i or j) not in disregardedValues):
                if (i not in disregardedValues):
                    disregardedValues = np.append(disregardedValues, i)
                if (currentStudent1[1] == currentStudent2[1]):
                    print(FAIL + "\nDuplicate in line " + str(j+1) + "! The same student ID and name are shared by " + str(currentStudent2[1]) 
                       + " in line " + str(i+1) + " and line " + str(j+1) + "!" + BACK)
                    disregardedValues = np.append(disregardedValues, j)
                    errorRows = np.append(errorRows, j+1)
                else:
                    print(FAIL + str(currentStudent1[1] + " in line " + str(i+1) + " and " + str(currentStudent2[1]) 
                        + " in line " + str(j+1) + " share the same student ID!") + BACK)
                    if (j not in errorRows):
                        errorRows = np.append(errorRows, j+1)
                errors = True
    if (errors == False):
        print(OK + "None" + BACK)
    return errorRows


# checkForGradeErrors FUNCTION - checks if any grades from a N x M matrix are not on the 7-step-scale
# and returns the indices where they were found.
#
# Usage: gradeErrors = checkForGradeErrors(data)
#
# Input: data - a N x M matrix
#
# Output: invalidGrades - an array which contains each erroreous grade and its position in the N x M matrix
#
# Author: Tudor Ciobanu

def checkForGradeErrors(data):
    N = np.size(data, axis = 0)  # N - number of students
    invalidGrades = np.empty([0,3]) # the erroreous grades and their positions in the data set
    print(WARNING + "\nGrade errors in the data set: " + BACK)
    errors = False #True if errors have been found and False otherwise
    for i in range(N):
        currentGrades = data[i,2:]
        for j in range(len(currentGrades)):
            if currentGrades[j] not in gradeScale:
                print(FAIL + "\n" + str(data[i,1]) + " (" + str(data[i,0]) + ") (line " + str(i+1) + ") has " + str(currentGrades[j])
                + " as one of his grades! Beware that this is not a grade on the 7-step-scale!" + BACK)
                row = np.array([currentGrades[j],i,j+2]) # an array that stores the grade, number of the row and column where it is encountered
                invalidGrades = np.vstack((invalidGrades, row))
                errors = True
    if (errors == False):
        print(OK + "None" + BACK)
    return invalidGrades


# deleteStudentRecord FUNCTION - deletes a row from a N x M matrix
#
# Usage: fullData = deleteStudentRecord(data, row)
#
# Input: data - a N x M matrix
#        row = a string representing the number of the row that is to be deleted
#
# Output: updatedData - the updated N x M matrix if a row has been deleted/the same matrix if no row is to be deleted
#
# Author: Tudor Ciobanu
                
def deleteStudentRecord(data, row):
    active = True # control variable for the loop below
    N = np.size(data, axis = 0) # N - number of students
    M = np.size(data, axis = 1) # M - number of assignments
    updatedData = np.empty([0,M]) # the matrix without the erroreous row
    while (active):
        answer = input(WARNING + "\nWould you like to delete row " + str(row) + " from the data set? " 
                       + BACK + "\nPlease type in " + OK + "yes" + BACK + " to confirm or " + FAIL + "no"
                       + BACK + " to cancel the operation. ")
        if (answer.lower() == "yes"):
            for i in range(N):
                if (i != row-1):
                    updatedData = np.vstack((updatedData, data[i,:]))
            print(OK + "\nThe record was successfully deleted! " + BACK)
            active = False
        elif (answer.lower() == "no"):
            print(FAIL + "\nOperation canceled!" + BACK)
            active = False
        else:
            print(WARNING + "\nUnknown command! Please try again! " + BACK)
    size = np.size(updatedData, axis = 0) # if the number of rows of the updated matrix is 0, then the operation was canceled, thus the original data shoudl be returned
    if (size == 0):
        updatedData = data
    return updatedData


# chooseRow FUNCTION - asks the user to select a specific row from a selection of rows
#
# Usage: row = chooseRow(rows)
#
# Input: rows - an array with the available rows
#
# Output: row - the row selected by the user/-1 if no row is selected
#
# Author: Tudor Ciobanu

def chooseRow(rows):
    active = True # control variable for the loop below
    while (active):
        row = -1 # by default the row chosen is -1
        print(WARNING + "\nThe following rows have issues: " + BACK)
        print(rows)
        answer = input("\nWould you like to delete any row?"
                       + "\nPlease type in " + OK + "yes" + BACK + " to confirm or " + FAIL + "no"
                       + BACK + " to cancel the operation. ")
        if (answer.lower() == "yes"):
            activeLoop = True
            while (activeLoop):
                print(WARNING + "\nThe following rows have issues: " + BACK)
                print(rows)
                selectedRow = input("\nPlease type the number of the row you would like to delete. Press exit to cancel the operation: ")
                if (is_number(selectedRow, "int") and int(selectedRow) in rows):
                    row = int(selectedRow) # the row is set to the input from the keyboard only if it is a number and it is one of the ones available
                    activeLoop = False
                    active = False
                elif (selectedRow.lower() == "exit"):
                    print(FAIL + "\nOperation canceled!" + BACK)
                    activeLoop = False
                    active = False
                else:
                    print(WARNING + "\nUnknown command! Please try again! " + BACK)
        elif (answer.lower() == "no"):
            print(FAIL + "\nOperation canceled!" + BACK)
            active = False
        else:
            print(WARNING + "\nUnknown command! Please try again! " + BACK)
    return row


# correctGradeData FUNCTION - corrects the grades so that all the grade in a N x M matrix are on the 7-step-scale
#
# Usage: fullData = correctGradeData(grades, data)
#
# Input: grades - an array with the erorreous grades and their positions in the matrix
#        data - a N x M matrix
#
# Output: data - a N x M matrix with all the grades on the 7-step-scale
#
# Author: Mihai Nipomici

def correctGradeData(grades, data):
    for i in range(len(grades)):
        row = grades[i]
        locationRow = int(row[1]) # the row in which it is encountered
        locationColumn = int(row[2]) # the column in which jt is encountered
        grade = row[0] # the grade itself
        if (locationRow < np.size(data, axis = 0)):
            data[locationRow,locationColumn] = roundGrade(np.array([grade]))[0] # the grade is changed to the closest grade from the 7-step-scale
            print(OK + "\nThe grades were successfully corrected!")
            print(OK + "\nGrades successfully changed!" + BACK)
        else:
            print(FAIL + "The row got deleted!" + BACK)
    return data


# loadData FUNCTION - asks the user for a filename for a csv file, loads the selected csv file and returns a
# a N x M matrix with all the data from the csv file
#
# Usage: fullData = loadData
#
# Output: fullData - a N x M matrix with all the data from the csv file/empty matrix if no file was found
# or the user canceled the operation
#
# Author: Tudor Ciobanu

def loadData():
    active = True
    fullData = np.array([])
    while (active):
        filename = input("\nPlease type in the name of the data file: ")
        potentialData = loadStudents(filename)
        if (np.size(potentialData, axis = 0) > 0):
            fullData = potentialData
            active = False
        else:
            activeLoop = True
            while (activeLoop):
                answer = input(WARNING + "\nWould you like to try again? Press yes to confirm or no to cancel the operation. " + BACK)
                if (answer == "no"):
                    activeLoop = False
                    active = False
                    print(FAIL + "\nOperation canceled!" + BACK)
                elif (answer == "yes"):
                    activeLoop = False
                else:
                    print(WARNING + "\nUnknown command. Please try again." + BACK)
    return fullData  


# deleteMultipleRecords FUNCTION - deletes muliple rows from a N x M matrix
#
# Usage: fullData = deleteMultipleRecords(data, indexes)
#
# Input: data - a N x M matrix
#        indexes - the index of the rows to be deleted
#
# Output: updatedData - a N x M matrix without the deleted rows
#
# Author: Tudor Ciobanu

def deleteMultipleRecords(data, indexes):
    N = np.size(data, axis = 0)
    M = np.size(data, axis = 1)
    updatedData = np.empty([0,M])
    for i in range(N):
        if (i+1 not in indexes):
            updatedData = np.vstack((updatedData, data[i,:]))
    print(OK + "\nThe records were successfully deleted! " + BACK)
    return updatedData


# displayGrades FUNCTION - displays each student from a N x M matrix in the alphabetical order,
# all of their grades, including their final grade
#
# Usage: displayGrades(data)
#
# Input: data - a N x M matrix
#
# Screen output: each student with all of her/his grades
#
# Author: Tudor Ciobanu

def displayGrades(data):
    data = data[data[:,1].argsort()]
    grades = data[:,2:]
    finalGrades = computeFinalGrades(np.array(grades, dtype = int))
    for i in range(np.size(data, axis = 0)):
        currentGrades = data[i,2:]
        output = "\n" + data[i,1] + "(" + data[i,0] + "): "
        for j in range(len(currentGrades)):
            output += str(currentGrades[j]) + ", "
        output += " final grade: " + str(finalGrades[i])
        print(output)
        

active = True # control variable for the loop below
print('\nWelcome to our program for grading students!')
fullData = loadData()
if (np.size(fullData, axis = 0) > 0): # if no data has been properly selected or is missing, the loop is stopped
    choice = printMenu()
    while (active):
        if (choice == '1'):
            data = loadData() # the data loaded from a csv file
            if (np.size(fullData, axis = 0) > 0):
                print(WARNING + "\nBeware that the data has not been changed!" + BACK)
                choice = printMenu()
            else:
                fullData = data # if the user confirms his/her action, the new data is the one loaded from the csv file
                choice = printMenu()
        elif (choice == '2'):
            errorRows = checkForDuplicateErrors(fullData)
            grades = checkForGradeErrors(fullData)
            choice = printMenu()
        elif (choice == '3'):
            grades = fullData[:,2:]
            gradesPlot(np.array(grades, dtype = int))
            choice = printMenu()
        elif (choice == '4'):
            displayGrades(fullData)
            choice = printMenu()
        elif (choice == '5'):
            if (len(errorRows) > 0):
                activeLoop = True
                while (activeLoop):
                    answer = input("Would you like to select one row to delete or all erroreous records? "
                                   + "Press 1 to select one row, 2 to delete all records or no to cancel the operation. ")
                    if (answer == "1"):
                        row = chooseRow(errorRows)
                        if (row != -1):  # if no row was selected, no row is to be deleted
                            fullData = deleteStudentRecord(fullData, row)
                            index = np.where(errorRows == row)
                            errorRows = np.delete(errorRows, index)
                            errorRows = errorRows - 1
                        activeLoop = False
                        choice = printMenu()
                    elif (answer == "2"):
                        loop = True
                        while(loop):
                            response = input("Are you sure? Press yes to confirm or no to cancel the operation!  ")
                            if (response == "yes"):
                                fullData = deleteMultipleRecords(fullData, errorRows)
                                errorRows = np.array([], dtype = int)
                                loop = False
                                activeLoop = False
                                choice = printMenu()
                            elif (response == "no"):
                                print(FAIL + "\nOperation canceled!" + BACK)
                                loop = False
                                activeLoop = False
                                choice = printMenu()
                            else:
                                print(WARNING + "\nUnknown command. Please try again." + BACK)
                    elif (answer == "no"):
                        print(FAIL + "\nOperation canceled!" + BACK)
                        activeLoop = False
                        choice = printMenu()
                    else:
                        print(WARNING + "\nUnknown command. Please try again." + BACK)
            elif (len(errorRows) == 0):
                print(WARNING + "\nNo errors found!" + BACK)
                print(WARNING + "\nPlease check for data errors first!" + BACK)
                choice = printMenu()
        elif (choice == '6'):
            if (len(grades) > 0):
                fullData = correctGradeData(grades, fullData)
            elif (len(grades) == 0):
                print(WARNING + "\nNo errors found!" + BACK)
                print(WARNING + "\nPlease check for data errors first!" + BACK)
            choice = printMenu()
        elif (choice == '7'):
            print(OK + "\nSee you next time!" + BACK)
            active = False
        else:
            print(WARNING + "\nUnknown command. Please try again." + BACK)
            choice = printMenu()
else:
    print(OK + "\nSee you next time!" + BACK)
