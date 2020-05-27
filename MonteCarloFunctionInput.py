import numpy as np
import numexpr as ne
import random
import matplotlib.pyplot as mtplt
import seaborn as sns

#set each of the input dictionaries as a function of one giant dictionary--see kanming

numRandVars = int(input("number of randomized variables: "))   #User input number of ranomdized vars
numSetVars = int(input("number of set variables: "))           #User input number of set variables


#Placeholder data to put in dictionary
randVarsExample = {"a": [1,100], "s": [2,30]}
setVarsExample = {"d": 10, "f":20}
numSimulatedTimeExample = 365
numSimulationsExample = 1000
equationExample = 'a**d+s*a'

allData = {"randVars": randVarsExample, "setVars": setVarsExample, "equation": equationExample,"numSimulatedTime": numSimulatedTimeExample,"numSimulations": numSimulationsExample}

randVars = allData.get("randVars")       #Randomized variables and their lower and upper bounds
setVars = allData.get("setVars")         #Set variables and their set values
allVars = {}                             #All variables, including randomized variables after their randomized value is determined--values assigned later

numSimulatedTime = allData.get("numSimulatedTime")
numSimulations = allData.get("numSimulations")
equation = allData.get("equation")                  #input must be expression




def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def uniformRandomize(randomVarArray):
    randomizedVarsArr = {}
    for key in randomVarArray:
        min = randomVarArray.get(key)[0]
        max = randomVarArray.get(key)[1]
        fixed = random.uniform(min,max)
        randomizedVarsArr.update({key:fixed})

    return randomizedVarsArr

def combineDicts(dict1,dict2):
    combinedDict = {}

    combinedDict.update(dict1)
    combinedDict.update(dict2)

    return combinedDict


def equationCalc(equationStr, variableDict):                        #Equivalent of the "simulated day" method in original MC sim
    return ne.evaluate(equationStr, global_dict = variableDict)

def unitSimulation(equationStr, randomVarDict, setVarDict , simulatedTime):       #Equivalent of "storage unit profit"
    valueTotal = 0
    valueArray = []
    valueArray.append(0)

    for x in range(simulatedTime):
        fullVarDict = combineDicts(setVars, uniformRandomize(randVars))

        valueTotal += equationCalc(equationStr,fullVarDict)
        valueArray.append(valueTotal)

    # print (valueArray)
    return valueArray

#The following is only necessary in the standalone code--when the frontend just sends dictionaries, this wont be necessary anymore:

for n in range(numRandVars):                                                                                                                                        #Input for all randomized variables, based on the number of variables user specified
    rangeArray = []
    newRandKey = input("Enter Your Randomized Variable Name (#" + str(n+1) + "): ")
    rangeArray.append(float(input(str(newRandKey) + " Lower Bound: ")))
    rangeArray.append(float(input(str(newRandKey) + " Upper Bound: ")))
    randVars[newRandKey]= rangeArray

for n in range(numSetVars):                                                                                                                                         #Input for all set variables, based on the number of variables user specified
    newSetKey = input("Enter Your Set Variable Name (#" + str(n+1) + "): ")
    setVars[newSetKey] = float(input((str(newSetKey) + " Set Value: ")))

#end of placeholder code

functionReplacements = {"sin": "numpy.sin", "cos": "numpy.cos", "tan": "numpy.tan", "log": "numpy.log", "exp": "numpy.exp"}                                              #need to include documentation for how to use certain functions (like log)
newEquation = replace_all(equation, functionReplacements)

timeArray = []
timeArray.append(0)
for time in range(numSimulatedTime):
    timeArray.append(time)


allSims = []
for sims in range(numSimulations):
    allSims.append(unitSimulation(equation,randVars,setVars,numSimulatedTime))

finalProfits = []
for simulation in range(len(allSims)):
    finalProfits.append(allSims[simulation][numSimulatedTime - 1])

print (finalProfits)

for sim in range(numSimulations):
    mtplt.plot(timeArray, allSims[sim])

mtplt.xlabel('Time (days)')
mtplt.ylabel('Profit ($)')
mtplt.draw()

mtplt.figure()
sns.distplot(finalProfits, hist=False, kde=True, label='Probability Density')
mtplt.xlabel('Profit ($)')
mtplt.ylabel('Probability Density')
mtplt.draw()

mtplt.show()

