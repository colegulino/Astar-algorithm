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

    print stringN + stringS + stringE + stringW

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
	#Find the x and y coordinates for the cell when initialized
        self.x = self.number % 7 - 1
        if self.x == -1:
            self.x = self.x % 7
        if self.number % 7 == 0:
            self.y = self.number / 7 - 1
        else:
            self.y = self.number / 7
            self.g = 0
            self.h = 0
            self.sum = 0
        print self.number, ": ", self.x, " ", self.y

    #Method for finding the next cell to move to
    def nextCell(self):
        self.gatherProxSensor()
        return self.findAdjacentHeuristics()

    #Gather proximity sensors from the map
    def gatherProxSensor(self):
        for cell in current_maze:
            if (cell.number == self.number):
                self.N = cell.N
                self.S = cell.S
                self.E = cell.E
                self.W = cell.W
		if (self.N == True):
			N = "True"
		else:
			N = "False"
		if (self.S == True):
			S = "True"
		else:
			S = "False"
		if (self.E == True):
			E = "True"
		else:
			E = "False"
		if (self.W == True):
			W = "True"
		else:
			W = "False"
		print "North: "+N+" South: "+S+" East: "+E+" West: "+ W

    def findAdjacentCells(self):
        if (self.number - 7 > 0):
            self.adjacentCells.append(findCell(self.number-7))
        else:
            self.adjacentCells.append(None)
        if (self.number + 7 < 50):
            self.adjacentCells.append(findCell(self.number+7))
        else:
            self.adjacentCells.append(None)
        if (self.number % 7 == 0):
            self.adjacentCells.append(None)
        else:
            self.adjacentCells.append(findCell(self.number+1))
        if (self.number % 7 == 1):
            self.adjacentCells.append(None)
        else:
            self.adjacentCells.append(findCell(self.number-1))

    def findAdjacentHeuristics(self):
        if (len(self.adjacentCells) == 0):
            print "Calling self.findAdjacentCells()"
            self.findAdjacentCells()
        cellHeuristics = []
        for cell in self.adjacentCells:
            #calculate heurstic value for each adjacent cell
            if (cell != None):
                ManhattanDistance = abs(cell.x-self.x)+abs(cell.y-self.y)+abs(endCell.x-cell.x)+abs(endCell.y-cell.y)
                cellHeuristics.append([ManhattanDistance,cell])
        #find the smallest heurstic cell and return
        for cell in cellHeuristics:
            minCell = None
            minHeur = 100000
            if (cell[0] < minHeur and cell[1] not in closedlist):
                minHeur = cell[0]
                minCell = cell[1]
        '''
        if (minCell == None):
            for cell in cellHeuristics:
                minCell = None
                minHeur = 100000
                if (cell[0] < minHeur):
                    minHeur = cell[0]
                    minCell = cell[1]
        '''
	print "Min cell: ", minCell
        return minCell



start_time = time.time()

maze_file = open('maze1.txt', 'r')
new_list = pickle.load(maze_file)
maze_file.close()


#Append the objects to the current maze list
print "========================================"
print "    Printing all of the maze squares    "
print "========================================"

current_maze = [] #Put all of the generated maze squares in an array
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


openlist = []
closedlist = []
#create cells for the start and end squares. Assume they are open at the start
startCell = Cell(startNumber, False, False, False, False)
endCell = Cell(endNumber, False, False, False, False)

#Set current cell to be the start cell
currentCell = startCell
count = 0
print "Initial Square: ", currentCell.number
#Run the Algorithm to go from start square to end square
'''
while (currentCell.number != endCell.number):
    #set the current cell to the next cell
    count += 1
    closedlist.append(currentCell)
    currentCell = currentCell.nextCell()
    print "Next square: ", str(currentCell.number), " Number of movements: ", str(count)
'''
closedlist.append(currentCell)
currentCell = currentCell.nextCell()
print "Next square: ", str(currentCell.number)
closedlist.append(currentCell)
currentCell = currentCell.nextCell()
print "Next square: ", str(currentCell.number)
closedlist.append(currentCell)
currentCell = currentCell.nextCell()
print "Next square: ", str(currentCell.number)



print "Final square: ", str(currentCell.number), " Number of movements: ", str(count)

print "Hello"

#Print How long the algorithm took to run
print "========================================"
print "Time to execute: ", (time.time()-start_time)
print "========================================"
