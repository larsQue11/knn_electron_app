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
def EuclideanDistance(testIris, knownIris):

    sumOfDifferences = 0
    if testIris.sepal_length != -1:
        sumOfDifferences = sumOfDifferences + ((testIris.sepal_length-knownIris.sepal_length) ** 2)
    if testIris.sepal_width != -1:
        sumOfDifferences = sumOfDifferences + ((testIris.sepal_width-knownIris.sepal_width) ** 2)
    if testIris.petal_length != -1:
        sumOfDifferences = sumOfDifferences + ((testIris.petal_length-knownIris.petal_length) ** 2)
    if testIris.petal_width != -1:
        sumOfDifferences = sumOfDifferences + ((testIris.petal_width-knownIris.petal_width) ** 2)

    return sqrt(sumOfDifferences)


#a function to evaluate the query against k neighbors
#returns a prediction based on the evaluation
def FindNeighbors(k,model,query):

    neighbors = []

    #calculate the Euclidean distance between the query and all Irises in the model
    #the neighbors array keeps a running track of the k nearest neighbors, it is sorted closest-furthest 
    #after each iteration, allowing the algorithm to test just the last position
    for iris in model:
        iris.setDistance(EuclideanDistance(query,iris))
        if len(neighbors) < k:
            neighbors.append(iris)
        else:
            if iris.distance < neighbors[k-1].distance:
                neighbors[k-1] = iris
        neighbors.sort(key=lambda x: x.distance)

    #find the mode amongst the classifications is found in the final list of neighbors
    numSetosas = 0
    numVersicolors = 0
    numVirginicas = 0
    for neighbor in neighbors:
        if neighbor.species == "Setosa":
            numSetosas = numSetosas + 1
        elif neighbor.species == "Versicolor":
            numVersicolors = numVersicolors + 1
        elif neighbor.species == "Virginica":
            numVirginicas = numVirginicas + 1

    if numSetosas > numVersicolors:
        if numSetosas > numVirginicas:
            prediction = "Setosa"
        else:
            prediction = "Virginica"
    else:
        if numVersicolors > numVirginicas:
            prediction = "Versicolor"
        else:
            prediction = "Virginica"

    return prediction


#a function that returns the index of the row for the corresponding species being tested
def UpdateTable(species):

    if species == "Setosa":
        dim = 0
    elif species == "Versicolor":
        dim = 1
    else:
        dim = 2

    return dim
        

#a custom object to represent the Iris's data values
class Iris():

    def __init__(self, irisData):
        self.sepal_length = float (irisData[0])
        self.sepal_width = float (irisData[1])
        self.petal_length = float (irisData[2])
        self.petal_width = float (irisData[3])
        self.distance = -1
        if len(irisData) > 4:
            if irisData[4] == 'Iris-setosa':
                self.species = 'Setosa'
            elif irisData[4] == 'Iris-versicolor':
                self.species = 'Versicolor'
            elif irisData[4] == 'Iris-virginica':
                self.species = 'Virginica'
        else:
            pass

    def setDistance(self, distance):
        self.distance = distance

    
def main():
    dataPath = './data/iris_dataset.csv'
    retrievedData = getData(dataPath)
    
    #create lists of Iris objects: half for training, half for testing
    trainingSet = []
    testingSet = []
    count = 0
    for iris in retrievedData:
        myIris = Iris(iris)
        if count % 2 == 0:
            trainingSet.append(myIris)
        else:
            testingSet.append(myIris)
        count = count + 1

    #build confusion matrix
    '''
    +------------+---------+------------+-----------+
    |            | Setosa  | Versicolor | Virginica |
    +------------+---------+------------+-----------+
    | Setosa     |  TP(S)  |   E(S,Ve)  |  E(S,Vi)  |
    | Versicolor | E(Ve,S) |   TP(Ve)   |  E(Ve,Vi) |
    | Virginica  | E(Vi,S) |   E(Vi,Ve) |   TP(Vi)  |
    +------------|---------+------------+-----------|
    '''
    confusionMatrix = np.zeros(shape=(3,3)) #creates a 2D array (3x3 table) containing all zeros
    
    #if input from user has been found, retrieve the input and set parameters
    if sys.argv[1]:
        #set K value
        k = int (sys.argv[1])

        #create an Iris
        userInput = [sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]]
        checkInput = sum(float (x) for x in userInput)
        userIris = Iris(userInput)
        
        #test the training model: update the confusion matrix for evaluation calculations
        for testIris in testingSet:

            #make a prediction for the current test case based on the specified K value and the model
            prediction = FindNeighbors(k,trainingSet,testIris)
            row = UpdateTable(testIris.species)
            col = UpdateTable(prediction)
            confusionMatrix[row,col] = confusionMatrix[row,col] + 1 #increment corresponding cell in the matrix
        
        #TP: the cell where the actual and predicted values intersect
        #TN: sum of all cells not in the classifier's row or column
        #FP: sum of all cells in the current column excluding TP
        #FN: sum of all cells in the current row excluding TP

        #calculate overall accuracy of model: (TP+TN)/(TP+TN+FP+FN)
        accuracy = (confusionMatrix[0,0] + confusionMatrix[1,1] + confusionMatrix[2,2]) / np.sum(confusionMatrix)
        accuracy = '{:.4}'.format(str(accuracy))

        #calculate precision: TP/(TP+FP)
        precisionSetosa = confusionMatrix[0,0] / np.sum(confusionMatrix,axis=0)[0]
        precisionSetosa = '{:.4}'.format(str(precisionSetosa))
        precisionVersicolor = confusionMatrix[1,1] / np.sum(confusionMatrix,axis=0)[1]
        precisionVersicolor = '{:.4}'.format(str(precisionVersicolor))
        precisionVirginica = confusionMatrix[2,2] / np.sum(confusionMatrix,axis=0)[2]
        precisionVirginica = '{:.4}'.format(str(precisionVirginica))

        #make prediction
        if checkInput > -4:
            prediction = FindNeighbors(k,trainingSet,userIris)
        else:
            prediction = "N/A"

        #print the output to an array which is returned to iris.js and then to the HTML document
        output = [k,prediction,accuracy,precisionSetosa,precisionVersicolor,precisionVirginica]
        for out in output:
            print(out)
        sys.stdout.flush()

    else:
        print(f"Nothing received")
        sys.stdout.flush()
    

if __name__ ==  '__main__':
    main()