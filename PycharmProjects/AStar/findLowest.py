import random

def lowestFcost(inputList):
    lowestValue = None
    lowList = []
    for index, i in enumerate(inputList):
        if lowestValue == None:
            lowestValue = i.f
        if i.f == lowestValue:
            lowList.append(index)
        elif i.f < lowestValue:
            lowList = [index]
            lowestValue = i.f
    if len(lowList) == 1:
        return lowList[0]
    return lowList[random.randint(0,len(lowList) - 1)]