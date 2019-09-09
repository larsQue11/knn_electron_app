import numpy as np
import math
import csv
import sys

def getData(dataPath):

    with open(dataPath) as dataFile:
        data = np.array(list(csv.reader(dataFile)))

    return data

def EuclideanDistance(testIris, knownIris):

    # if testIris.sepal_length == -1:
    #     testIris.sepal_length = knownIris.sepal_length
    # if testIris.sepal_width == -1:
    #     testIris.sepal_width = knownIris.sepal_width
    # if testIris.petal_length == -1:
    #     testIris.petal_length = knownIris.petal_length
    # if testIris.petal_width == -1:
    #     testIris.petal_width = knownIris.petal_width

    # sumOfDifferences = (
    #           ((testIris.sepal_length-knownIris.sepal_length) ** 2)
    #         + ((testIris.sepal_width-knownIris.sepal_width) ** 2)
    #         + ((testIris.petal_length-knownIris.petal_length) ** 2)
    #         + ((testIris.petal_width-knownIris.petal_width) ** 2))

    sumOfDifferences = 0
    if testIris.sepal_length != -1:
        sumOfDifferences = sumOfDifferences + ((testIris.sepal_length-knownIris.sepal_length) ** 2)
    if testIris.sepal_width != -1:
        sumOfDifferences = sumOfDifferences + ((testIris.sepal_width-knownIris.sepal_width) ** 2)
    if testIris.petal_length != -1:
        sumOfDifferences = sumOfDifferences + ((testIris.petal_length-knownIris.petal_length) ** 2)
    if testIris.petal_width != -1:
        sumOfDifferences = sumOfDifferences + ((testIris.petal_width-knownIris.petal_width) ** 2)

    return math.sqrt(sumOfDifferences)

def FindNeighbors(k,model,query):

    neighbors = []

    for iris in model:
        iris.setDistance(EuclideanDistance(query,iris))
        if len(neighbors) < k:
            neighbors.append(iris)
        else:
            if iris.distance < neighbors[k-1].distance:
                neighbors[k-1] = iris
        neighbors.sort(key=lambda x: x.distance)

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

def UpdateTable(species):

    if species == "Setosa":
        dim = 0
    elif species == "Versicolor":
        dim = 1
    else:
        dim = 2

    return dim
        

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
    confusionMatrix = np.zeros(shape=(3,3))
    
    if sys.argv[1]:
        # #set K value
        k = int (sys.argv[1])

        #create an Iris based off the user input paramaters
        userInput = [sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]]
        userIris = Iris(userInput)
        

        for testIris in testingSet:

            prediction = FindNeighbors(k,trainingSet,testIris)
            row = UpdateTable(testIris.species)
            col = UpdateTable(prediction)

            confusionMatrix[row,col] = confusionMatrix[row,col] + 1
        
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

        prediction = FindNeighbors(k,trainingSet,userIris)

        output = [k,prediction,accuracy,precisionSetosa,precisionVersicolor,precisionVirginica]
        for out in output:
            print(out)
        sys.stdout.flush()

    else:
        print(f"Nothing received")
        sys.stdout.flush()
    

if __name__ ==  '__main__':
    main()