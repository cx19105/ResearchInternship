import matplotlib.pyplot as plt

def testConcentration(dataList):
    sourceOne = dataList[0]
    sourceTwo = dataList[1]
    sourceThree = dataList[2]
    sourceOneSum = []
    sourceTwoSum = []
    sourceThreeSum = []
    x = []
    count = 0

    for timeStep in range(0, len(sourceOne)-1):
        x.append(timeStep)
        sourceOneSum.append(sum(sum(sourceOne[timeStep])))
        sourceTwoSum.append(sum(sum(sourceTwo[timeStep])))
        sourceThreeSum.append(sum(sum(sourceThree[timeStep])))

    plt.plot(x, sourceOneSum, 'r-', sourceTwoSum, 'b-', sourceThreeSum, 'g-')
    plt.legend(['Source 1', 'Source 2','Source 3'])
    plt.show()

