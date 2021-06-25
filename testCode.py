import matplotlib.pyplot as plt

def testConcentration(dataList):
    sourceOne = dataList[0]
    sourceTwo = dataList[1]

    sourceOneSum = []
    sourceTwoSum = []
    x = []
    count = 0

    for timeStep in range(0, len(sourceOne)):
        count += 1
        sourceOneSum.append(sum(sum(sourceOne[timeStep])))
        sourceTwoSum.append(sum(sum(sourceTwo[timeStep])))
        x.append(count)
    
    plt.plot(x, sourceOneSum, 'r-', sourceTwoSum, 'b-')
    plt.legend(['Source 1', 'Source 2'])
    plt.show()

