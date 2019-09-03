import numpy as np
import math
import csv
import sys

def getData(dataPath):

    with open(dataPath) as dataFile:
        data = np.array(list(csv.reader(dataFile)))

    # #sort the dataset into the three categories
    # row, col = np.where(data == 'Iris-setosa')
    # dataSetosa = np.take(data,row,0)

    # # self.dataVersicolor = []
    # row, col = np.where(data == 'Iris-versicolor')
    # dataVersicolor = np.take(data,row,0)

    # # self.dataVirginica = []
    # row, col = np.where(data == 'Iris-virginica')
    # dataVirginica = np.take(data,row,0)

    # return dataSetosa, dataVersicolor, dataVirginica
    return data

def EuclideanDistance(testIris, knownIris):

    if testIris.sepal_length == -1:
        testIris.sepal_length = knownIris.sepal_length
    if testIris.sepal_width == -1:
        testIris.sepal_width = knownIris.sepal_width
    if testIris.petal_length == -1:
        testIris.petal_length = knownIris.petal_length
    if testIris.petal_width == -1:
        testIris.petal_width = knownIris.petal_width

    sumOfDifferences = (
              ((testIris.sepal_length-knownIris.sepal_length) ** 2)
            + ((testIris.sepal_width-knownIris.sepal_width) ** 2)
            + ((testIris.petal_length-knownIris.petal_length) ** 2)
            + ((testIris.petal_width-knownIris.petal_width) ** 2))

    return math.sqrt(sumOfDifferences)

        

class Iris():

    def __init__(self, irisData):
        self.sepal_length = float (irisData[0])
        self.sepal_width = float (irisData[1])
        self.petal_length = float (irisData[2])
        self.petal_width = float (irisData[3])
        self.distance = -1
        if irisData[4] == 'Iris-setosa':
            self.species = 'Setosa'
        elif irisData[4] == 'Iris-versicolor':
            self.species = 'Versicolor'
        elif irisData[4] == 'Iris-virginica':
            self.species = 'Virginica'

    def setDistance(self, distance):
        self.distance = distance

    
def main():
    dataPath = '../data/iris_dataset.csv'
    # Setosas, Versicolors, Virginicas = getData(dataPath)
    retrievedData = getData(dataPath)
    # print(Setosas)
    # print(Versicolors)
    # print(Virginicas)
    
    ListOfIrises = []
    for iris in retrievedData:
        myIris = Iris(iris)
        ListOfIrises.append(myIris)

    if sys.argv[1]:
    # myIris = [4.9,3.6,1.1,0.3]
        userInput = [sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]]
        userIris = Iris(userInput)

        for iris in ListOfIrises:
            iris.setDistance(EuclideanDistance(myIris,iris))

        # Neighbors = np.sort(ListOfIrises,0,kind='quicksort',Iris.distance)
        Neighbors = sorted(ListOfIrises, key=lambda Iris: Iris.distance)
    

        print(f"The closest Neighbor is: ")
        sys.stdout.flush()

    else:
        print(f"Nothing received")
        sys.stdout.flush()
    

if __name__ ==  '__main__':
    main()