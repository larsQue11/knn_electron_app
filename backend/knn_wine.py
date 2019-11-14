# Course: CS7267
# Student name: William Stone
# Student ID: 000-272-306
# Assignment #: 1
# Due Date: September 16, 2019
# Signature:
# Score:

import numpy as np
from math import sqrt
import csv
import sys

#retrieve data from CSV file
def getData(dataPath):

    with open(dataPath) as dataFile:
        data = np.array(list(csv.reader(dataFile)))

    return data


#calculate the Euclidean distance: sqrt( sum( (x.i - y.i)^2 ) )
def EuclideanDistance(testWine, knownWine):

    #create dictionaries of the objects to make their paramaters iterable
    testWineDict = vars(testWine)
    knownWineDict = vars(knownWine)

    sumOfDifferences = 0

    for key,value in testWineDict.items():
        if value != -1: #if a value was not provided, it's passed as -1 so we can ignore it
            difference = value - knownWineDict[key]
            difference = difference ** 2
            sumOfDifferences = sumOfDifferences + difference

    return sqrt(sumOfDifferences)


#a function that finds the k nearest neighbors of the query when it is inserted into the model
#neighors is a list that tracks the k nearest neighbors sorted by closest distance, if a closer 
#neighbor is found, it replaces the last in the list
#since this is a regression problem, the prediction is made by taking the median of the neighbors
def FindNeighbors(k,model,query):

    neighbors = []

    for wine in model:
        wine.setDistance(EuclideanDistance(query,wine))
        if len(neighbors) < k:
            neighbors.append(wine)
        else:
            if wine.distance < neighbors[k-1].distance:
                neighbors[k-1] = wine
        neighbors.sort(key=lambda x: x.distance)

    totalDistance = 0
    for wine in neighbors:
        totalDistance = totalDistance + wine.distance
    prediction = totalDistance / k

    return prediction

        
#a custom object representing the attributes for a wine
class Wine():

    def __init__(self, wineData):
        self.fixed_acidity = float (wineData[0])
        self.volatile_acidity = float (wineData[1])
        self.citric_acid = float (wineData[2])
        self.residual_sugar = float (wineData[3])
        self.chlorides = float (wineData[4])
        self.free_sulfur_dioxide = float (wineData[5])
        self.total_sulfur_dioxide = float (wineData[6])
        self.density = float (wineData[7])
        self.pH = float (wineData[8])
        self.sulphates = float (wineData[9])
        self.alcohol = float (wineData[10])
        if(len(wineData) == 12):
            self.quality = float (wineData[11])
        else:
            self.quality = 0
        self.distance = -1

    def setDistance(self, distance):
        self.distance = distance

    
def main():
    dataPath = './data/whitewinequality_dataset.csv'
    retrievedData = getData(dataPath)

    #create lists of Wine objects: half for training, half for testing
    trainingSet = []
    testingSet = []
    count = 0
    for wine in retrievedData:
        myWine = Wine(wine)
        if count % 2 == 0:
            trainingSet.append(myWine)
        else:
            testingSet.append(myWine)
        count = count + 1

    #if input from user has been found, retrieve the input and set parameters
    if sys.argv[1]:
        #set K value
        k = int (sys.argv[1])

        #create a Wine object from the user input
        userInput = [x for x in sys.argv[2:]]
        checkInput = sum(float (x) for x in userInput)
        userWine = Wine(userInput)

        #test the training model, calculating values for Mean Squared Error, Root Mean Squared Error,
        #and Mean Absolute Error
        sumOfSquaredDifferences = 0
        sumOfAbsoluteDifferences = 0
        for testWine in testingSet:

            prediction = FindNeighbors(k,trainingSet,testWine)
            difference = prediction - testWine.quality
            sumOfSquaredDifferences = sumOfSquaredDifferences + (difference ** 2)
            sumOfAbsoluteDifferences = sumOfAbsoluteDifferences + abs(difference)

        meanSquaredError = sumOfSquaredDifferences / len(testingSet)
        rootMeanSquaredError = sqrt(meanSquaredError)
        meanAbsoluteError = sumOfAbsoluteDifferences / len(testingSet)

        #make prediction
        if checkInput > -11:
            prediction = FindNeighbors(k,trainingSet,userWine)
            prediction = '{:.4}'.format(str(prediction))
        else:
            prediction = "N/A"

        meanSquaredError = '{:.4}'.format(str(meanSquaredError))
        rootMeanSquaredError = '{:.4}'.format(str(rootMeanSquaredError))
        meanAbsoluteError = '{:.4}'.format(str(meanAbsoluteError))

        #print the output to an array which is returned to wine.js and then to the HTML document
        output = [k,prediction,meanSquaredError,rootMeanSquaredError,meanAbsoluteError]
        for out in output:
            print(out)
        sys.stdout.flush()
        
    else:
        print(f"Nothing received")
        sys.stdout.flush()


if __name__ ==  '__main__':
    main()