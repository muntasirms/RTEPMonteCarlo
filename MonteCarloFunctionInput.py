import numpy as np
import numexpr as ne
import random
import matplotlib.pyplot as mtplt
import seaborn as sns

#https://numexpr.readthedocs.io/projects/NumExpr3/en/latest/user_guide.html numexpr library supported functions

#Placeholder data to put in dictionary
randVarsExample = {"a": [-200,-100], "s": [-20,-30]}
setVarsExample = {"d": 10, "f":20}
numSimulatedTimeExample = 365
numSimulationsExample = 1000
equationExample = 'a^d-s*a-log(a)'

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



functionReplacements = { "^": "**"}                                              #need to include documentation for how to use certain functions (like log)
newEquation = replace_all(equation, functionReplacements)
print(newEquation)

timeArray = []
timeArray.append(0)
for time in range(numSimulatedTime):
    timeArray.append(time)


allSims = []
for sims in range(numSimulations):
    allSims.append(unitSimulation(newEquation,randVars,setVars,numSimulatedTime))

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

