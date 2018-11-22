# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 11:23:32 2018

@author: User
"""

import numpy as np
from roundgrade_function import roundGrade
from final_grade_func import computeFinalGrades
from grades_plot_function import gradesPlot


dataLoaded = False   # Specifies is data has been loaded or not
fullData = None   # This variable will eventually contain the data loaded from the dataLoad function


def printMenu():
    print("\nMenu:")
    print("1. Load new data.")
    print("2. Check for data errors.")
    print("3. Generate plots.")
    print("4. Display list of grades.")
    print("5. Quit.")
    choice = input("Please type in the number of the operation you would like to perform:  ")
    return choice

def gradesMenu():
    print('\nGrades Menu:')
    print('1. Display grades for each assignment.')
    print('2. Display final grade for all of the students.' )
    print('3. Back to main menu.')
    choice = input("Please type in the number of the operation you would like to perform:  ")
    return choice

def assignmentMenu():
    print('\nAssignment Menu:')
    choice = input("Please type in the number of the operation you would like to perform:  ")
    return choice

print('\nWelcome to our Program for grading students!')
choice = printMenu()

def loadCSV(filename):
    data = np.array([])
    try:
        data= np.loadtxt(filename, delimiter=",", skiprows=1)
    except IOError:
        print("Unable to open the file with the following name: " + filename+"! Please try again with a different filename! ")
    return data




active = True   # control variable for the loop below
while(active):
    if choice == "1":
        filename = input("Type in the name of the file you would like to use:  ")
        possibleData = loadCSV(filename)
        while(np.size(possibleData) == 0):                    
            answer = input("Do you want to try again? Type in yes or no:  ")
            if (answer.lower() == "yes"):
                filename = input("Type in the name of the file you would like to use:  ")
                possibleData=loadCSV(filename)
            elif (answer.lower() == "no"):
                choice = printMenu()
                break
        if (np.size(possibleData) > 0):
            dataLoaded = True
            fullData=possibleData
            numberOfStudents=np.size(fullData, axis=0)
            numberOfAssignments= np.size(fullData, axis=1) - 2
            print('Number of students: '+ str(numberOfStudents))
            print('Number of assignments: '+ str(numberOfAssignments))     
            print("\nData loaded successfully!")
            choice = printMenu()
    elif choice == "2":
        printActiveFilter()
        if (dataLoaded == True):
            answer = printFilterMenu()
            runningFilter = True
            while (runningFilter):
                if answer == "1":
                    bacteriaChoice = printBacteriaMenu()
                    runningBacteriaFilter = True
                    while(runningBacteriaFilter):
                        if (dataFiltered[0] == True and dataFiltered[1] == True):
                            bacteriaFound = False
                            print("An existing filter for both bacteria and growth rate already exists.")
                            print("By changing the bacteria filter, the exisiting growth rate filter will be removed.")
                            confirmation = input("Do you want to continue? Type in yes to confirm. Any other input will be disregarded and you will be taken to the main menu.  ")
                            if (confirmation == "yes"):
                                for i in range(len(bacterias)):
                                    if (int(bacteriaChoice)-1 == i):
                                        indices = np.where(fullData[:,2] == bacterias[i])
                                        currentData = fullData[indices]
                                        bacteriaFound = True
                                        dataFiltered[0] = True
                                        dataFiltered[1] = False
                                        print("\nBacteria filter successfully added.")
                                        runningBacteriaFilter = False
                                        runningFilter = False
                                        choice = printMenu()
                                        break
                                if (bacteriaFound == False):
                                    print("\nUnknown command. Please try again.")
                                    bacteriaChoice = printBacteriaMenu()
                            else:
                                runningBacteriaFilter = False
                                runningFilter = False
                                choice = printMenu()
                        else:
                            bacteriaFound = False
                            for i in range(len(bacterias)):
                                if (int(bacteriaChoice)-1 == i):
                                    indices = np.where(fullData[:,2] == bacterias[i])
                                    currentData = fullData[indices]
                                    bacteriaFound = True
                                    dataFiltered[0] = True
                                    print("\nBacteria filter successfully added.")
                                    runningBacteriaFilter = False
                                    runningFilter = False
                                    choice = printMenu()
                                    break
                            if (bacteriaFound == False):
                                print("\nUnknown command. Please try again.")
                                bacteriaChoice = printBacteriaMenu()
                elif answer == "2":
                    lowerBound = input("Please input the lower bound:  ")
                    upperBound = input("Please input the upper bound:  ")
                    runningGrowthFilter = True
                    while(runningGrowthFilter):
                        if (is_number(lowerBound, "float") and is_number(upperBound, "float")):
                            difference = float(upperBound) - float(lowerBound)
                            if (difference > 0 and difference < 1):
                                growthRates = currentData[:,1].astype(np.float)
                                indices = np.array([], dtype = int)
                                for i in range(len(growthRates)):
                                    if (growthRates[i] >= float(lowerBound) and growthRates[i] <= float(upperBound)):
                                        indices = np.append(indices, i)
                                currentData = currentData[indices]
                                dataFiltered[1] = True
                                print("\nGrowth rate filter successfully added.")
                                runningGrowthFilter = False
                                runningFilter = False
                                choice = printMenu()
                            elif (difference < 0):
                                print("Invalid values for upper and lower bounds. The lower bound cannot be bigger or equal to the upper bound!")
                                confirmation = input("Would you want to try again? Type in yes to confirm. Any other input will be disregarded and you will be taken to the main menu.  ")
                                if (confirmation == "yes"):
                                    lowerBound = input("Please input the lower bound:  ")
                                    upperBound = input("Please input the upper bound:  ")
                                else:
                                    runningGrowthFilter = False
                                    runningFilter = False
                                    choice = printMenu()
                        else:
                            print("Please type in integers for both the lower and upper bound!")
                            confirmation = input("Would you want to try again? Type in yes to confirm. Any other input will be disregarded and you will be taken to the main menu.  ")
                            if (confirmation == "yes"):
                                lowerBound = input("Please input the lower bound:  ")
                                upperBound = input("Please input the upper bound:  ")
                            else:
                                runningGrowthFilter = False
                                runningFilter = False
                                choice = printMenu()
                elif answer == "3":
                    runningFilter = False
                    currentData = fullData
                    dataFiltered[0] = False
                    dataFiltered[1] = False
                    print("\nFilter removed successfully!")
                    choice = printMenu()
                elif answer == "4":
                    runnningFilter = False
                    choice = printMenu()
                else:
                    print("\nUnkown command. Please try again.")
                    answer = printFilterMenu()
        else:
            print("\nData is not loaded yet! Please load the data first!")
            choice = printMenu()
    elif (choice == "3"):
        if (dataLoaded == True):
            gradesPlot(grades)
            choice=printMenu()
        else:
            print("\nData is not loaded yet! Please load the data first!")
            choice = printMenu()
    elif (choice == "4"):
        if (dataLoaded == True):
            answer= gradesMenu()
            if answer == 1:
                sdfsdfasf
            elif answer == 2:
                grades= np.array([])
                for i in range(len(fullData)):
                    currentRow= fullData[i,:]
                    currentRow= currentRow[2: len(currentRow)]
                    grades= np.append(grades, currentRow)
                grades= computeFinalGrades(grades)
                print('\nFinal grades for all students:')
                print(grades)
            elif answer == 3:
                choice = printMenu()            
        else:
            print("\nData is not loaded yet! Please load the data first!")
            choice = printMenu()
    elif (choice == "5"):
        print("\nThank you for using Bacteria Analysis interactive program!")
        active = False
    else:
        print("\nUnkown command. Please try again.")
        choice = printMenu()

