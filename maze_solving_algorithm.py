# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:55:39 2015

@author: Cole Gulino
"""

import numpy as np
import pickle, sys
import time

def findCell(cellNo):
    for cell in current_maze:
        if cell.number == cellNo:
            return cell

def printAdjacent(adjacentCells):
    if (adjacentCells[0] == None):
        stringN = "North: None"
    else:
        stringN = "North: " + str(adjacentCells[0].number)
    if (adjacentCells[1] == None):
        stringS = " South: None "
    else:
        stringS = " South: " + str(adjacentCells[1].number)
    if (adjacentCells[2] == None):
        stringE = " East: None "
    else:
        stringE = " East: " + str(adjacentCells[2].number)
    if (adjacentCells[3] == None):
        stringW = " West: None"
    else:
        stringW = " West: " + str(adjacentCells[3].number)

    return stringN + stringS + stringE + stringW

def printAdjacentStart(adjacentCells):
    if (adjacentCells[0] == True):
        stringN = "North: True "
    else:
        stringN = "North: False "
    if (adjacentCells[1] == True):
        stringS = " South: True "
    else:
        stringS = " South: False "
    if (adjacentCells[2] == True):
        stringE = " East: True "
    else:
        stringE = " East: False "
    if (adjacentCells[3] == True):
        stringW = " West: True "
    else:
        stringW = " West: False "

    return stringN + stringS + stringE + stringW

def printClosedList(list):
    string = ""
    for cell in list:
        string += str(cell.number) + " "

    return string

class Cell:
    def __init__(self, number, N, S, E, W):
        #Cell object to hold all of the cells in the maze
        self.number = number # Number in the maze
        #T or F if there is a wall on N, S, E, or W side of the wall
        self.N = N
        self.S = S
        self.E = E
        self.W = W
        self.adjacentCells = []
        self.direction = ""
        #Find the x and y coordinates for the cell when initialized
        self.x = self.number % 7 - 1
        if self.x == -1:
            self.x = self.x % 7
        if self.number % 7 == 0:
            self.y = self.number / 7 - 1
        else:
            self.y = self.number / 7
        self.openlist = []
        self.ManhattanDistance = 10000
        print self.number, ": ", self.x, " ", self.y, printAdjacentStart([self.N, self.S, self.E, self.W])

    #Method for finding the next cell to move to
    def nextCell(self):
        self.gatherProxSensor()
        self.findDirection()
        return self.findPath()

    #Gather proximity sensors from the map
    def gatherProxSensor(self):
        for cell in current_maze:
            if (cell.number == self.number):
                self.N = cell.N
                self.S = cell.S
                self.E = cell.E
                self.W = cell.W

    def findAdjacentCells(self):
        #Get North
        if (self.N == True):
            self.adjacentCells.append(None)
        elif (self.number - 7 < 0):
            self.adjacentCells.append(None)
        else:
            self.adjacentCells.append(findCell(self.number-7))
        #Get South
        if (self.S == True):
            self.adjacentCells.append(None)
        elif (self.number + 7 > 50):
            self.adjacentCells.append(None)
        else:
            self.adjacentCells.append(findCell(self.number+7))
        #Get East
        if (self.E == True):
            self.adjacentCells.append(None)
        elif (self.number % 7 == 0):
            self.adjacentCells.append(None)
        else:
            self.adjacentCells.append(findCell(self.number+1))
        #Get West
        if (self.W == True):
            self.adjacentCells.append(None)
        elif (self.number % 7 == 1):
            self.adjacentCells.append(None)
        else:
            self.adjacentCells.append(findCell(self.number-1))

    def findDirection(self):
        self.direction = ""
        if (self.y > endCell.y):
            self.direction += "North"
        elif (self.y < endCell.y):
            self.direction += "South"
        if (self.x < endCell.x):
            self.direction += "east"
        elif (self.x > endCell.x):
            self.direction += "west"

        print "===================================================="
        print "Cell: ", self.number, " Direction: ", self.direction

    def findPath(self):
        if (len(self.adjacentCells) == 0):
            #print "Calling self.findAdjacentCells()"
            self.findAdjacentCells()


        for cell in self.adjacentCells:
            if (cell != None and cell != prevCell and cell not in self.openlist):
                self.openlist.append(cell)
            if (cell == endCell):
                #Check to see if the final square is around the robot
                return cell

        nextCell = None

        while (nextCell == None):
            if (len(self.openlist) == 0):
                #3 wall case, chose the previous square
                print "3 wall case"
                self.chosen = prevCell
                nextCell = prevCell
            elif (len(self.openlist) == 1):
                #2 wall case, choose only one in the list
                self.chosen = self.openlist[0]
                nextCell = self.openlist[0]
                print "2 wall case"
            #elif (len(self.openlist) == 2 or len(self.openlist) == 3):
            else:
                #1 wall case or no wall case
                print "1 wall case or no wall case"
                newlist = []
                for cell in self.openlist:
                    if (cell not in closedlist):
                        newlist.append(cell)
                if (len(newlist) == 1):
                    #if theres one thats not in close list, chose it
                    self.chosen = newlist[0]
                    nextCell = self.chosen
                elif (len(newlist) == 0):
                    #if both are in closed list chose the one you havent chosen before
                    for cell in self.openlist:
                        if (cell != self.chosen):
                            self.chosen = cell
                            nextCell = self.chosen
                else:
                    #If neither are in closed list, chose the one closer to the final square
                    for cell in self.openlist:
                        #calculate Manhattan Distance for each cell in self.openlist
                        cell.ManhattanDistance = abs(cell.x-self.x)+abs(cell.y-self.y)+abs(endCell.x-cell.x)+abs(endCell.y-cell.y)
                    #find minimum Manhattan Distance
                    nextCell = min(self.openlist, key=lambda cell: cell.ManhattanDistance)

        print "AC: ", printAdjacent(self.adjacentCells)
        print "Open List: ", printClosedList(self.openlist)

        return nextCell



start_time = time.time()

maze_file = open('maze2.txt', 'r')
new_list = pickle.load(maze_file)
maze_file.close()


#Append the objects to the current maze list
print "========================================"
print "    Printing all of the maze squares    "
print "========================================"

current_maze = [] #Put all of the generated maze squares in an array
print current_maze
for item in new_list:
    cell = Cell(item[0], item[1], item[2], item[3], item[4])
    current_maze.append(cell)

#Get the start and end cells
file3 = open('start_end.txt', 'r')
numbers = file3.read().splitlines()
startNumber = int(numbers[0])
endNumber = int(numbers[1])



print "========================================"
print "         Beginning A* Algorithm         "
print "========================================"
print "Start square: ", startNumber, "  End square: ", endNumber

closedlist = []
nextrun = []
direction = ""
#create cells for the start and end squares. Assume they are open at the start
startCell = findCell(startNumber)
endCell = findCell(endNumber)

if (startCell.x < endCell.x):
    direction = "right"
else:
    direction = "left"

#Set current cell to be the start cell
currentCell = startCell
count = 0
print "Initial Square: ", currentCell.number
#Run the Algorithm to go from start square to end square
closedlist.append(currentCell)
prevCell = None

while (currentCell != endCell):
    #set the current cell to the next cell
    count += 1
    tempCell = currentCell
    currentCell = currentCell.nextCell()
    if (count > 100):
        break
    prevCell = tempCell
    print str(currentCell.number)
    closedlist.append(currentCell)

print "Final square: ", str(currentCell.number), " Number of movements: ", str(count)

#Print How long the algorithm took to run
print "========================================"
print "Time to execute: ", (time.time()-start_time)
print "========================================"
